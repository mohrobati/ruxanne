This is the supplementary material for Ruxanne, a big fix pattern miner for Rust as described in the paper "A Study of Common Bug Fix Patterns in Rust".

It contains the modules for parsing, code embedding, mining and clustering, as well as the final results to help others understand, replicate, and extend our work. Open an issue or submit a PR to help us improve Ruxanne.


<h1>Installation</h1>
<ul>
<li>Install Python packages in requirements.txt</li>

```
pip install -r requirements.txt
```
<li>Install cargo---1.64.0-nightly (a5e08c470 2022-06-23)</li>
https://doc.rust-lang.org/cargo/getting-started/installation.html
</ul>

<h1>Files/Directory Structure</h1>

<ul>
<li>
implementation
<ul>
<li>1-mining</li>
<ul>
<li><b>parser</b>: Includes programs we used to parse Rust files (rust-parser) and transform them to json format (syn_compiler). We wrote our own transformer to transform Syn AST to json. We could have used syn_serde to do this serialization for us, but we figured in this way, we'd end up storing more information. Also, we have implemented the path extraction logic here (ddiff.py)</li>
<li><b>embedding</b>: Includes code regarding our embedding approach (RQ1 contains the environment we used to carry out the experiment for evaluating our embedding effectiveness)</li>
<li><b>scheme</b>: Contains our weighting scheme (weight_adjustments.json) and how we computed it (weight.py).</li>
<li>circle_pack.py: Visualizing the essence of each change (read the paper for more info)</li>
<li><b>freq.py</b>: Recording the # Occurrences of all the non terminals from the 20 recent commits within the target repositoreis</li>
<li><b>miner.py</b>: Mining all the target repositories and converting them to clusterable embeddings</li>
<li><b>test.py</b>: A test mining for only one single commit, all the results will be written in implementation/1-mining/__logs__</li>
<li><b>projects.txt</b>: List of all target repositories</li>
</ul>
<li>2-clustering: All the scripts we used to run the DBSCAN on our datasets.
<ul>
<li><b>borrow_only.csv.zip</b>: After unzipping, the csv file contains D<sub>b</sub> as discussed in the paper</li>
<li><b>total.csv.zip</b>: After unzipping, the csv file contains D<sub>g</sub> as discussed in the paper</li>
<li><b>borrow_only.ipynb</b>: Jupyter Notebook file used to cluster D<sub>b</sub></li>
<li><b>total.ipynb</b>: Jupyter Notebook file used to cluster D<sub>g</sub></li>
<li><b>dbscan_stats.py</b>: Visualizing different clusterings with different parameters</li>
</ul>
<li>3-results: Contains all the information with regards to the final clusters.
    <ul>
    <li><b>Overview.csv</b>: A general overview of all the clusters</li>
    <li><b>BC.ref.add.csv</b>: Information of all the datapoints within the cluster <i>Adding Borrowing</i> (read the paper for more info about this cluster)</li>
    <li>Similar for other cluster...</li>
    </ul>
</li>
</ul>

</li>
</ul>