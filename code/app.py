import streamlit as st
import pandas as pd
import os
import tempfile
import sys
import plotly.express as px
import plotly.graph_objects as go
from assertion_extractor import clone_github_repo, get_test_files, analyze_file, extract_repo_name


st.set_page_config(page_title="Python Test Assertion Extractor", layout="wide")
st.title("Python Test Assertion Extractor")
st.markdown("""
This app extracts test assertions from Python GitHub repositories and generates a CSV report.
Enter a GitHub repository URL to analyze its test assertions.
""")

github_url = st.text_input("Enter GitHub Repository URL")

progress_placeholder = st.empty()
result_placeholder = st.empty()

if st.button("Extract Assertions"):
    if not github_url or not github_url.startswith("https://github.com/"):
        st.error("Please enter a valid GitHub repository URL")
    else:
        
        progress_bar = progress_placeholder.progress(0)
        
        with st.spinner("Cloning repository..."):
            
            try:
                repo_dir = clone_github_repo(github_url)
                progress_bar.progress(25)
                
              
                test_files = get_test_files(repo_dir)
                st.info(f"Found {len(test_files)} test files")
                progress_bar.progress(50)
                
             
                all_assertions = []
                file_count = len(test_files)
                
                for i, file_path in enumerate(test_files):
                    file_assertions = analyze_file(file_path)
                    all_assertions.extend(file_assertions)
                    # progress bar updation logic
                    progress_percent = 50 + int((i / file_count) * 40)
                    progress_bar.progress(min(90, progress_percent))
                
              
                if all_assertions:
                    df = pd.DataFrame(all_assertions)
                    progress_bar.progress(95)
                    
                   
                    repo_name = extract_repo_name(github_url)
                    csv_data = df.to_csv(index=False)
                    
                    progress_bar.progress(100)
                    progress_placeholder.empty()
                    
                   
                    result_placeholder.success(f"Found {len(all_assertions)} assertions in {file_count} files")
                    
                    
                    tab1, tab2, tab3 = st.tabs(["Data", "Visualizations", "Statistics"])
                    
                    with tab1:
                        
                        st.subheader("Assertion Data")
                        st.dataframe(df, use_container_width=True)
                        
                        
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"{repo_name}_assertions.csv",
                            mime="text/csv"
                        )
                    
                    with tab2:
                        st.subheader("Visualization Dashboard")
                        
                       
                        col1, col2 = st.columns(2)
                        
                        with col1:
                           
                            #Assertions per file (top 10)
                            file_counts = df['filepath'].value_counts().reset_index().head(10)
                            file_counts.columns = ['Filepath', 'Count']
                            
                            file_counts['Filename'] = file_counts['Filepath'].apply(lambda x: os.path.basename(x))
                            
                            # bar chart for file dist
                            fig1 = px.bar(
                                file_counts, 
                                x='Count', 
                                y='Filename',
                                title='Top 10 Files by Assertion Count',
                                orientation='h',
                                color_discrete_sequence=['#3366CC']
                            )
                            fig1.update_layout(yaxis={'categoryorder':'total ascending'})
                            st.plotly_chart(fig1, use_container_width=True)
                            
                        with col2:
                            # pie chart
                            if 'testclass' in df.columns and df['testclass'].notna().sum() > 0:
                              
                                class_counts = df[df['testclass'] != '']['testclass'].value_counts().reset_index()
                                class_counts.columns = ['Test Class', 'Count']
                               
                                top_classes = class_counts.head(10)
                                if len(class_counts) > 10:
                                    others_count = class_counts['Count'][10:].sum()
                                    others_df = pd.DataFrame({'Test Class': ['Others'], 'Count': [others_count]})
                                    class_counts_pie = pd.concat([top_classes, others_df])
                                else:
                                    class_counts_pie = top_classes
                                
                                fig2 = px.pie(
                                    class_counts_pie, 
                                    values='Count', 
                                    names='Test Class',
                                    title='Assertion Distribution by Test Class',
                                    hole=0.4,
                                )
                                st.plotly_chart(fig2, use_container_width=True)
                            else:
                                st.info("No test class data available for visualization")
                        
                       
                        col3, col4 = st.columns(2)
                        
                        with col3:
                           
                            def categorize_assertion(assert_str):
                                assert_str = assert_str.lower()
                                if "equal" in assert_str:
                                    return "Equality"
                                elif "true" in assert_str:
                                    return "Boolean True"
                                elif "false" in assert_str:
                                    return "Boolean False"
                                elif "raise" in assert_str or "exception" in assert_str:
                                    return "Exception"
                                elif "in" in assert_str:
                                    return "Membership"
                                elif "is" in assert_str and "not" in assert_str:
                                    return "Identity Not"
                                elif "is" in assert_str:
                                    return "Identity"
                                elif "greater" in assert_str or ">" in assert_str:
                                    return "Greater Than"
                                elif "less" in assert_str or "<" in assert_str:
                                    return "Less Than"
                                else:
                                    return "Other"
                            
                            df['assertion_type'] = df['assert_string'].apply(categorize_assertion)
                            type_counts = df['assertion_type'].value_counts().reset_index()
                            type_counts.columns = ['Assertion Type', 'Count']
                            
                            fig3 = px.bar(
                                type_counts,
                                x='Assertion Type',
                                y='Count',
                                title='Assertion Types Distribution',
                                color='Assertion Type',
                            )
                            st.plotly_chart(fig3, use_container_width=True)
                        
                        with col4:
                            
                            df['directory'] = df['filepath'].apply(lambda x: os.path.dirname(x).split('/')[-1] if '/' in x else 'root')
                            dir_counts = df['directory'].value_counts().reset_index().head(15)
                            dir_counts.columns = ['Directory', 'Count']
                            
                            fig4 = px.treemap(
                                dir_counts,
                                path=['Directory'],
                                values='Count',
                                title='Assertion Concentration by Directory',
                                color='Count',
                                color_continuous_scale='Blues',
                            )
                            st.plotly_chart(fig4, use_container_width=True)
                    
                    with tab3:
                        st.subheader("Assertion Statistics")
                        
                       
                        stat_col1, stat_col2, stat_col3 = st.columns(3)
                        
                        with stat_col1:
                            
                            st.metric("Total Assertions", len(df))
                        
                        with stat_col2:
                            
                            avg_per_file = round(len(df) / len(df['filepath'].unique()), 2)
                            st.metric("Avg. Assertions per File", avg_per_file)
                        
                        with stat_col3:
                            
                            if 'testclass' in df.columns:
                                test_class_count = len(df[df['testclass'] != '']['testclass'].unique())
                                st.metric("Unique Test Classes", test_class_count)
                            else:
                                st.metric("Unique Test Classes", 0)
                        
                        st.subheader("Top Test Functions")
                        func_counts = df['testname'].value_counts().head(10).reset_index()
                        func_counts.columns = ['Test Function', 'Assertion Count']
                        st.dataframe(func_counts, use_container_width=True)
                        
                        
                        st.subheader("Files with Most Assertions")
                        file_stats = df.groupby('filepath').agg({
                            'line_number': 'count', 
                            'testname': 'nunique',
                            'testclass': lambda x: x[x != ''].nunique()
                        }).reset_index()
                        file_stats.columns = ['Filepath', 'Assertion Count', 'Unique Test Functions', 'Unique Test Classes']
                        file_stats = file_stats.sort_values('Assertion Count', ascending=False).head(10)
                        file_stats['Filename'] = file_stats['Filepath'].apply(lambda x: os.path.basename(x))
                        st.dataframe(file_stats[['Filename', 'Filepath', 'Assertion Count', 'Unique Test Functions', 'Unique Test Classes']], use_container_width=True)
                    
                else:
                    progress_placeholder.empty()
                    result_placeholder.warning("No assertions found in this repository")
                
               
                import shutil
                shutil.rmtree(repo_dir, ignore_errors=True)
                
            except Exception as e:
                progress_placeholder.empty()
                result_placeholder.error(f"Error: {str(e)}")


with st.expander("How it works"):
    st.markdown("""
    ### How the Assertion Extractor Works
    
    1. **Clone Repository**: The tool clones the specified GitHub repository to a temporary directory
    2. **Identify Test Files**: It locates Python files that appear to contain tests (based on filename and directory)
    3. **Parse Code**: Each test file is parsed into an Abstract Syntax Tree (AST)
    4. **Extract Assertions**: The tool traverses the AST to find assertion statements and methods
    5. **Generate Report**: Results are compiled into a CSV with file paths, test classes, test names, line numbers, and assertion strings
    
    ### Visualizations
    
    The dashboard provides multiple views of your assertion data:
    
    - **Top Files**: Bar chart showing which files contain the most assertions
    - **Test Class Distribution**: Pie chart showing how assertions are distributed across test classes
    - **Assertion Types**: Analysis of common assertion patterns (equality, boolean, etc.)
    - **Directory Concentration**: Treemap showing which directories contain the most assertions
    
    ### Supported Assertion Types
    
    - Standard Python `assert` statements
    - unittest assertion methods (`assertEqual`, `assertTrue`, etc.)
    - Common test framework assertions
    """)