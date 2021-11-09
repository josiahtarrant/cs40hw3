# Hello! Welcome to my third homework!
## At a high level, this file scrapes item data off ebay for a specific search term.
### Here is a more specific explanation of what this `ebay-dl.py` file does:
1. The file takes the search term from the command line
1. The file downloads ten pages of results from ebay for the supplied search term 
1. The file extracts all of the items from the ebay search results
1. The file creates a python list of each item with dictionary keys for name, price, status, shipping cost, free return options, and items sold
1. The file saves the list as a new json file specific to that search term

### Here are the commands I ran to get my three json files for the terms *'longboard'*, *'book'* and *'Apple watch'*:

<pre><code>python3 ebay-dl.py longboard
</code></pre>
<pre><code>python3 ebay-dl.py book 
</code></pre>
<pre><code>python3 ebay-dl.py 'apple watch'
</code></pre>

### **Lastly,** [here](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03) is the link to this assignment!