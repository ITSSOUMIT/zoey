### hi Zoey <img src="https://raw.githubusercontent.com/ABSphreak/ABSphreak/master/gifs/Hi.gif" width="30px">

Say hello to **zoey**, a command line based Static Site Generator !

**zoey** is based on [Python](https://www.python.org/), and works on any Python installation above `v3.6.x`

#### Contents
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Core concepts](#core-concepts)
- [Usage](#usage)

#### Installation
1. Install Python for your OS from <a href="https://www.python.org/downloads/" target="_blank">here</a>
2. Ensure that **Add Python to PATH** checkbox during installation is **checked**.
3. Open a command line of your choice, type `pip install zoey` and press enter ⏎

Voila, thats it ! **zoey** is installed and ready to go.

#### Getting Started
To create a new site, in your command line of choice, type
`zoey new site <site-name>`
This command generates a folder named `<site-name>`, with the following structure -
```
/<site-name>
├── config.py
├── /public
└── /src
    ├── /assets
    │   ├── /media
    │   └── style.css
    └── index.md
```

Folder structure explanation -
1. `config.py` - This file holds certain configuration for your site.
2. `/src` - This is the folder where you will be writing all the pages for your site in markdown `.md` format.
3. `/public` - This is the folder, which will have the final html files, which you can directly copy and add to any hosting service of choice. The contents of this folder will be auto generated when the generator is run.

#### Core concepts
1. Always make changes in the src directory only. **No direct changes to be made to the public directory.**
2. group - A group is basically a folder inside src, which groups some pages together.
3. page - A page is an individual markdown file, that will be converted to a HTML page.
4. All multimedia files should be placed inside the `src/assets/media` folder only, and then suitably linkedin inside the markdown files.

#### Usage
1. To create a new page -
   ```bash
   zoey new page <page-name>
   ```
   This creates a new page named `page-name.md` inside the src folder.
2. To create a group -
   ```bash
   zoey new group <group-name>
   ```
   This creates a new folder named `group-name` inside the src folder.
   > **assets** is a reserved keyword for group naming, and cannot be used to create any group 
3. To create a new page inside a group -
   ```bash
   zoey new page <page-name> --group <group-name>
   ```
   This creates a new page named `page-name.md` inside the `group-name` folder.
4. To see the list of all groups -
   ```bash
   zoey groups
   ```
   This lists down all the groups that have been created.
5. To generate the final site -
    ```bash
    zoey generate site
    ````
    This will populate the public directory which can be copied and added to any hosting provider of choice.

#### Hope you enjoy using zoey
**zoey** is the brainchild of [Soumit Das](https://www.linkedin.com/in/itssoumit)
To report bugs, please send a bug report, along with python and pip version number to [me@soumit.in](mailto:me@soumit.in)