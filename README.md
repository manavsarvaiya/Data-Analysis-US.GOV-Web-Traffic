# Data-Analysis-US.GOV-Web-Traffic
A Python data analysis project exploring a public dataset from Bitly and USA.gov. This dataset contains anonymous records of users who shortened .gov and .mil links in 2012.

The analysis focuses on deriving user demographics—specifically geographic location and technology stack—from raw web access logs.

Key Insights
The project answers two main questions:

Where are the users? Inferred from time zone data.

What do they use? Determined by parsing User-Agent strings.

The findings reveal a user base predominantly in U.S. Eastern and Central time zones, primarily using Mozilla-based browsers on Windows machines.

Tech Stack
Python with pandas for data manipulation, numpy for logic, and matplotlib for visualization.
