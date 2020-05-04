# Contributing to the `BISTRO` Starter Kit

The core development team and maintainers are always grateful to users looking to improve this starter kit. In order to equitably, expeditiously, and courteously resolve issues as well as collaborate on improvements to the code base, we ask that you adhere to the guidelines below.

## What should I know before I get started?
### Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [Jessica Lazarus](mailto:jlaz@berkeley.edu).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for the `BISTRO` Starter Kit. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.

Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#writing-a-good-bug-report). If you'd like, you can use [this template](#template-for-submitting-bug-reports) to structure the information.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

* **Check the [FAQs Page](docs/FAQ.md)** for a list of common questions and problems.
* **Perform a [cursory search](https://github.com/vgolfier/Uber-Prize-Starter-Kit/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+)** to see if the problem has already been reported. If it has, add a comment to the existing issue instead of opening a new one.

#### Writing a (Good) Bug Report


Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). After going through [the necessary first steps](#before-submitting-a-bug-report), you can create an issue on GitHub and provide the following information.

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. For example, start by explaining how you started the simulation evaluation, e.g. which command exactly you used in the terminal, or how you started the simulation evaluation otherwise. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem. If you use the keyboard while following the steps, **record the GIF with the [Keybinding Resolver](https://github.com/atom/keybinding-resolver) shown**. You can use [this tool](http://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **If you're reporting a crash**, include a crash report with a stack trace from the operating system. Include the crash report in the issue in a [code block](https://help.github.com/articles/markdown-basics/#multiple-lines), a [file attachment](https://help.github.com/articles/file-attachments-on-issues-and-pull-requests/), or put it in a [gist](https://gist.github.com/) and provide link to that gist.
* **If the problem is related to performance**, include a [CPU profile capture and a screenshot](http://flight-manual.atom.io/hacking-atom/sections/debugging/#diagnose-performance-problems-with-the-dev-tools-cpu-profiler) with your report.
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new `SNAPSHOT` version, as of 05/01/2020, the latest version is `0.0.3-noacc-SNAPSHOT`) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version of the snapshots?** 
	* `0.0.3-saving-SNAPSHOT` and `0.0.3-SNAPSHOT` is available to pull for testing as well.
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version of the snapshot image are you using?** 
	*	If you are using the example Jupyter Notebook, locate the `competition_executor.py` file (/utilities/competition_executor.py) and find the `IMAGE_TAG` field. 
* **Are you running `BISTRO` in a virtual machine?** If so, which VM software are you using and which operating systems and versions are used for the host and the guest?

#### Template For Submitting Bug Reports

    [Short description of problem here]

    **Reproduction Steps:**

    1. [First Step]
    2. [Second Step]
    3. [Other Steps...]

    **Expected behavior:**

    [Describe expected behavior here]

    **Observed behavior:**

    [Describe observed behavior here]

    **Screenshots and GIFs**

    ![Screenshots and GIFs which follow reproduction steps to demonstrate the problem](url)

    **SNAPSHOT version:** [Enter SNAPSHOT version here]
    **OS and version:** [Enter OS name and version here]

    **Additional information:**

    * Problem started happening recently, didn't happen in an older version of the SNAPSHOT: [Yes/No]
    * Problem can be reliably reproduced, doesn't happen randomly: [Yes/No]

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for the `BISTRO` Starter Kit, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:.

Before creating enhancement suggestions, please check [this list](#before-submitting-an-enhancement-suggestion) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion). If you'd like, you can use [this template](#template-for-submitting-enhancement-suggestions) to structure the information.

#### Before Submitting An Enhancement Suggestion

* **Perform a [cursory search](https://github.com/vgolfier/Uber-Prize-Starter-Kit/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)** to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
<!--* TODO: Add more pre-requisites for enhancement suggestion-->

#### Submitting a (Good) Enhancement Suggestion

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). After going through [the necessary first steps](#before-submitting-an-enhancement-suggestion), you can create an issue on and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of the starter kit that the suggestion is related to. You can use [this tool](http://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** to most `BISTRO` users.
* **List some other similar open source projects or applications where this enhancement exists.**
* **Which version of the snapshot image are you using?** 
	*	If you are using the example Jupyter Notebook, locate the `competition_executor.py` file (/utilities/competition_executor.py) and find the `IMAGE_TAG` field. 
* **Specify the name and version of the OS you're using.**

#### Template For Submitting Enhancement Suggestions

    [Short description of suggestion]

    **Steps which explain the enhancement**

    1. [First Step]
    2. [Second Step]
    3. [Other Steps...]

    **Current and suggested behavior**

    [Describe current and suggested behavior here]

    **Why would the enhancement be useful to most users**

    [Explain why the enhancement would be useful to most users]

    [List some other similar open source projects or applications where this enhancement exists]

    **Screenshots and GIFs**

    ![Screenshots and GIFs which demonstrate the steps or part of BISTRO the enhancement suggestion is related to](url)

    **OS and Version:** [Enter OS name and version here]
### Your First Code Contribution

    Unsure where to begin contributing to this starter kit? You can start by looking through these `beginner` and `help-wanted` issues:

    * [Beginner issues][beginner] - issues which should only require a few lines of code, and a test or two.
    * [Help wanted issues][help-wanted] - issues which should be a bit more involved than `beginner` issues.

    Both issue lists are sorted by total number of comments. While not perfect, number of comments is a reasonable proxy for impact a given change will have.

    If you want to read about using BEAM, you can have a quick look through these resources in the documentation.

### Pull Requests

* Include screenshots and animated GIFs in your pull request whenever possible.
* End files with a newline.
<!--TODO: Add more pre-requisites for Pull Requests.-->
<!--TODO: Add Documentation Styleguide.-->

## Styleguides

### Python Style


Beyond standard PEP8 conventions, we try to follow the
[Google Python style guide](https://google.github.io/styleguide/pyguide.html) with the significant exception that we use the [numpy documentation style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html). 
 


### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally
* When only changing documentation, include `[ci skip]` in the commit description
* Consider starting the commit message with an applicable emoji: (TODO: Needs review)
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :non-potable_water: `:non-potable_water:` when plugging memory leaks
    * :memo: `:memo:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on macOS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    <!--* :green_heart: `:green_heart:` when fixing the CI build-->
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings


## Additional Notes

### Development Guidelines

Current developers should follow the [workflow](#workflow-for-developers) below.

We use a scrumboard on [waffle.io](https://waffle.io/sfwatergit/BeamCompetitions). Opening an issue or pull request will result in labeling the issue or PR. In order to take advantage of the automated labeling and referencing functionality of this tool, we make extensive use of several issue cross-referencing in GitHub.

#### Workflow for Developers

1. **Naming a Branch**: Branches are named `<your_initials_or_gh_username>/#<issue_number>-<short_issue_title_in_lower_snake_case>`. Doing so and pushing the branch to GitHub moves the issue from `Inbox` to `In Progress` on the board and assigns the corresponding label.
2. **Creating a Pull Request**: Pull requests **must** either address or close an existing issue. When closing an issue, the description of the PR must contain the word *closes* followed by the issue number (e.g., "closes #12"). Using "closes" will automatically close the corresponding issue (i.e., move it to done together with the pull request) when merging to master. When addressing an issue, the description of the PR must contain the word *connects* followed by the issue number (e.g., "connects #12"). Using "connects" will *not* automatically close the issue when merging to master.
3. **Code Reviews**: No PRs will be merged to master prior to receiving a review by someone who did not submit the PR. When submitting a PR, please designate an appropriate reviewer. If review is blocking progress and is not completed in a timely manner, please try to (politely) ping the reviewer. Contact the technical team leads [Jessica Lazarus](mailto:jlaz@berkeley.edu) or [Jarvis Yuan](mailto:jarviskroos7@berkeley.edu) for assistance if problems persist.

## Need Help & Immediate Support?

If the above seems daunting to you, please feel free to reach out to the
[`BISTRO`](http://bistro.its.berkeley.edu/) team or contact the team lead directly:
* Jessica Lazarus: [jlaz@berkeley.edu](mailto:jlaz@berkeley.edu)
* Jarvis Yuan: [jarviskroos7@berkeley.edu](mailto:jarviskroos7@berkeley.edu)

## Attribution
We thank crowdAI (@crowdAI) for suggesting the template for this documentation, which itself was adapted from the [Atom](https://atom.io) project's [Contributor Guidelines](https://github.com/atom/atom/blob/master/CONTRIBUTING.md).

## Thank you!

:+1: :tada:  Thanks for taking the time to contribute! :tada: :+1:
