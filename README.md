# The Plan

I'm excited to get into orchestrating data pipelines, and part of the journey for me will be implementing one from scratch.  This is the tentative plan for the project.  

Note: Credit to this comment for a great structure to follow! https://old.reddit.com/r/dataengineering/comments/g1dody/data_engineering_syllabus/fneyvpx/

1. Write a scraper that pulls the top 25 posts on the /r/wow subreddit each day.

2. Put the scraper in a docker container and host it inside gitlab container registry.

3. Spin up a Kubernetes cluster on a cloud service provider.

4. Use helm to deploy Airflow inside your Kubernetes cluster

5. Write a dag and use Airflow to instantiate your Scraper, then scrape posts. You should set this scraper to run daily.

6. Store raw data from your scraper inside a Minio server running inside your kubernetes cluster

7. Use spark to read in the raw data from the Minio server, clean the data, and insert it into a Postgres database. (also running in your Kubernetes cluster)
