# mdx-include-lines

This is a markdown extension for python. It will allow you to include lines from a source file or a whole source file in your Markdown document. This project is based on [simonrenger/markdown-include-lines](https://github.com/simonrenger/markdown-include-lines). I added some tweaks I needed. :) 

## What can you do with this extension? 

- include a whole file 
- include only a certain line 
- include certain lines 
- include a certain range of lines (e.g. 5-29) 

## How to use this extension 

Replace [...] with the right content. The examples below are kindof templates. :) 

```markdown
{type * [startline]-[endline] filename  caption  show_linenums}
```

### Parameters explained 

- `type`: the type of the file, used to highlight the included block properly 
- `*`: if you use the asterisc, the whole file will be included 
- `startline` (optional): use this together with `endline`, with a dash (-) between them, to specify a range of lines to be included 
- `endline` (optional): use this together with `startline`, with a dash (-) between them, to specify a range of lines to be included 
- `filename`: the name of the source file which will be included 
- `caption`: a description/caption of the source file; *the two spaces before and after the caption are REQUIRED*. The caption can have multiple words, with some interpunction, you don't need to surround it with quotes.
- `show_linenums`: use 0 to hide or 1 to show the line numbers to the left of the lines 

### Examples 

Include the whole file: 

```markdown
{python * include.py  A function written in Python  1}
```

Include only one line: 

```markdown
{python 15 include.py  The return line  0}
```

Include only certain lines of code: 

```markdown
{python [15,20,3] include.py  All return expressions  1}
```

Include a range of lines: 

```markdown
{python 15-20 include.py  An example of a Python function  1}
```


## Installation and usage 

### Installation 

You can install this extension directly with pip: 

```bash
$ pip install git+https://github.com/vlajna95/mdx-include-lines.git
```

Or clone this repo and then run: 

``` bash
cd /wherever/the/files/are
$ pip install .
```

### Example usage in Python code 

Here is a simple example, with Markdown extension configurations. Of course, in a real situation you'll use other extensions like `meta` or `tables`, and you'll probably choose a different style, but I'm showing just the configurations required in order to use all the capabilities of Markdown syntax highlighting. 
It might be important to mention that this requires *pymdown-extensions* and *pygments* to be installed. 

```python
from markdown import Markdown

md_extension_configs = {
	"pymdownx.details": {},
	"pymdownx.superfences": {"preserve_tabs": True},
	"pymdownx.highlight": {"css_class": "highlight", "use_pygments": True, "noclasses": True, "pygments_style": "colorful"},
	"mdx_include_lines": {"base_path": ".", "encoding": "utf-8"}
}
md_extensions = [e for e in md_extension_configs.keys()]
md = Markdown(extensions=md_extensions, extension_configs=md_extension_configs, output_format="html5")

md_source = """Include a source file: 

{python * hello.py  A short file with some greetings  0}
"""

print(md.convert(md_source))
```

### Example HTML output (source) 

```html
<p>Include a source file: </p>
<details>
<summary>A short file with some greetings</summary>
<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><code><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;Hello all!&quot;</span>)
<span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;I really like Markdown. And you? :)&quot;</span>)
</code></pre></div>
</details>
```

### Example HTML output (rendered) 

<p>Include a source file: </p>
<details>
<summary>A short file with some greetings</summary>
<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><code><span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;Hello all!&quot;</span>)
<span style="color: #007020">print</span>(<span style="background-color: #fff0f0">&quot;I really like Markdown. And you? :)&quot;</span>)
</code></pre></div>
</details>
