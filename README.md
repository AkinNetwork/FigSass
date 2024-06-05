# FigSass Smart Contract

Project name: _FigSass Smart Contract_

This endeavor revolves around transforming Figma JSON variables into a SCSS variable framework. We'll employ a smart contract to streamline the process of converting Figma variable JSON exports into a corresponding array of variables, which will then be integrated into a SCSS file.

Author's note: While we draw upon the principles of Ethereum smart contracts, this project does not pertain to blockchain Ethereum smart contracts. Instead, it operates as a mini-application based on smart contract principles.

## The Algorithm

1. Set-up Python environment.
   1. Check the and update the installed Python version.
   2. requisites: Homebrew: <https://brew.sh/> - installed with `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)`
2. FigSass Smart Contract **algorithm:**
   1. Read the Figma JSON file using a python data object
   2. Export data into a file with extension .scss
   3. Check and validate the imported JSON file as Figma variable JSON file
   4. Format the variables as SCSS variables and save them into \_variables.scss file
