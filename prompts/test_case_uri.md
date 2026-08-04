# Test case with URI OPeNDAP server

Read the CLAUDE.md file to gain context about the project.

# Primary objective

Perform an exploratory analysis of data in a URI OPeNDAP server.  Use this URL to access data at URI: https://sst-aqua.gso.uri.edu/opendap/

# Additional context

This document contains information about OPeNDAP and pydap:
~/Git\_Repos/grep-dap/docs/opendap\_readme.tex

# Latex

Make a log of any of your commands and of your thoughts in a Latex file named test\_case\_uri\_log\_prompt\_#.tex in the ~/Git\_Repos/grep-dap/docs/ directory, where # is the number of the prompt in the test\_case\_uri.md file .  Be sure to add a timestamp any time (including time of day) that you add a new section to the log.

Generate a standlone LateX file named uri\_test\_case\_prompt\_#.tex in the ~/Git\_Repos/grep-dap/docs/ directory that describes your findings.

# Scripts

If you will execute a series of Python commands, save them in a file named <script\_name>.py in the ~/Git\_Repos/grep-dap/scripts/ directory.


# Prompts

1. Read this document.  Explore the contents of the URI OPeNDAP server.  Describe the data and the metadata.  Describe the data within the server and explain your reasoning.  Be mindful of the overall project that we are working on.  Spend up to 1 hour on this task.  

2. This is an excellent start. Reread this document and the *\_1.tex files produced with the first prompt so that you are familiar with the work you have already completed related to this project.

    Next, I would like you to generate a table for Readable Branch #1: SST\_Orbits/. For each variable in the dataset, indicate whether the semantic (COARDS) metadata essential for using that variable are complete. If the metadata are complete, state that explicitly. If they are incomplete, list the missing COARDS metadata and provide your best guess for what the values should be.

    In addition, identify, again for each variable, any semantic metadata that are not strictly required by COARDS but that you believe would significantly facilitate use and interpretation of the dataset.

    In the next prompt, we will repeat this process for Readable Branch #2: gradients\_by\_period/.

3. Perfect. Now, reread this document and documentation produced while executing prompts 1-2 so that you are familiar with the work you have already completed related to this project.

   Next, I would like you to repeat the above for Readable Branch #2: gradients\_by\_period/. Since this archive has no semantic metadata, you will have to infer whatever you can. I suggest that you group the semantic metadata by inferred values for which you are very confident, those for which you are not sure but have guessed at entries and those for which you do not feel comfortable guessing. You should also group these by essential and 'would be nice'.

4. Perfect. Now, reread this document and documentation produced while executing prompts 1-3 so that you are familiar with the work you have already completed related to this project. 

    Then, estimate the spatial range over which the gradients were calculated for branch  #2 and explain how you arrived at he answer. This information will be used in the next prompt.
    
5. The estimates of spatial range over which the gradients were calculated look good. Now, as for previous prompts, read the outputs and then write a description of each of the two datasets for a typical user; i.e., not too detailed but detailed enough for the user to decide whether or not the dataset meets their needs and to acquire subsets of the data in which they might be interested. Also, provide usage_sst.md and usage_gradient_SST.md files, which the user can provide to an AI agent to acquire and make use of the data.

6. Reread this document and documentation produced while executing prompts 1-5 so that you are familiar with the work you have already completed related to this project. 

    Then, produce Latex doducments, one for each dataset, directed to the curators of the two datasets, describing what is missing related to the semantic metadata. These documents should be short and to the point.
    
7. Reread this document and documentation produced while executing prompts 1-6 so that you are familiar with the work you have already completed related to this project. Then write project_summary.tex, a .tex file summarizing what was done and why, and put the file in the top level of the project. This file should be written in such a way that it could be used as the basis for a portion of a proposal related to this approach to help curators of NASA Earth Science archives to validate and update the metadata of archives for which they are responsible as well as to facilitate the use of these archives by the research community.
    
8. Reread this document and the documentation you have generated. There are a few issues, which need to be addressed: 
a) You did not address the metadata for the latitude and longitude of the L2eqa fields in the SST\_Orbits\_dataset. Please do so. 
b) I would like you to take a stab at how fields in the L2eqa\_grid, in the SST\_Orbits dataset, were constructed.
c) I would like you to take a stab at identifying the origin of the fields, which were summed for the gradients\_by\_period dataset. 
d) When you have completed the above, write updated, \_2, versions of project\_summary.tex, curator\_report\_gradients\_by\_period.tex, curator\_report\_sst\_orbits.tex, usage\_gradient\_SST.md and usage\_sst.md in addition to the appropriate test\_case\_uri\_log\_7.tex file.
e) Finally, delete all \*.aux, \*.log and \*.out files in the project but be careful not to delete the test\_case\_uri\_log\_\*.tex and test\_case\_uri\_log\_\*.pdf files.

<!-- 4. Now, reread this document and documentation produced while executing prompts 1-3 so that you are familiar with the work you have already completed related to this project.
 
    Next,I would like you to write six files and place all of them in the output directory. The first two are a reports to be written for the curator(s)s of each of the readable brances summarizing the results of the semantic metadata surveys. This document can refer to the ouput of prompt #3 if needed
    
 3. Thanks.  Can you configure the COARDS per-variable attributes in Section 6.3.3 of uri\_test\_case.tex to follow what was done for the coordinates?  Also, Table 6 has overlapping text between columns.  Please fix that too.

4. Given the semantic metatadat that you have generated for the gradients\_by\_period dataset, can you provide a description of the data and how it was generated?  Add to the uri\_test\_case.tex file accordingly.  If you need to do any additional analysis, please do so and add to the log file and the uri\_test\_case.tex file accordingly.


8. Reread this document and documentation produced while executing prompts 1-7 so that you are familiar with the work you have already completed related to this project. 

    NASA's primary search engine for datasets is EarthData Search.  Please generate an entry for EarthData Search that describes the gradients\_by\_period dataset.  Generate a new file for this that conforms to the EarthData Search format.
-->