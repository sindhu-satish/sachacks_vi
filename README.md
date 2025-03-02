## Career Compass AI
Choosing a career is tough! Our AI-based platform offers personalized real-time trend analysis, & hands-on simulations helping students explore careers, gain insights, and make confident choices!

## Inspiration
Choosing a career is overwhelming. Students often lack proper guidance, real-world exposure, and access to up-to-date industry trends. Traditional career counseling methods are often outdated and generic. We wanted to leverage AI to create a smarter, more personalized, and data-driven career exploration platform—one that empowers students with real insights and hands-on experience.

## What it does
Career Compass AI is an AI-powered career exploration platform that:
1. Assesses students' interests and strengths through interactive AI-driven quizzes.
2. Analyzes real-time industry trends from platforms like Reddit and Medium.
3. Provides hands-on career simulations and domain-specific challenges.
4. Uses AI-based recommendations to match students with the best career paths.

## How we built it
We engineered Career Compass AI by integrating multiple cutting-edge technologies to create an intelligent, dynamic, and user-friendly platform. Our frontend is built with React and TypeScript, leveraging Tailwind CSS for a responsive and visually appealing design that adapts seamlessly across devices. On the backend, a Flask API orchestrates the flow of data and user requests, acting as the critical bridge between the UI and our core AI functionalities. For generating personalized career insights, we harness the power of GPT-3.5 and LLaMA 3—GPT-3.5 enables natural, conversational interactions while LLaMA 3 supports detailed, data-driven recommendations. We built a robust **database using ChromaDB to efficiently store and retrieve our curated career data, ensuring our retrieval-augmented generation (RAG) system delivers real-time, contextually relevant advice. To populate this knowledge base, we developed custom web scraping pipelines: one script uses the Google Custom Search API and BeautifulSoup to extract relevant Medium articles, while another leverages PRAW to collect posts from key career-focused subreddits. This integrated approach allows us to continuously update and scale our platform, providing users with personalized, up-to-date career guidance.

## Challenges we ran into
1. Processing real-time career trends while ensuring data accuracy.
2. Optimizing AI recommendations for personalized and relevant career matches.
3. Ensuring seamless frontend-backend integration for a smooth user experience.
4. Creating engaging and meaningful simulations for hands-on career exposure.

## Accomplishments that we're proud of
1. Successfully built an AI-driven platform that personalizes career guidance.
2. Integrated real-time industry trend analysis to provide up-to-date insights.
3. Developed a modern, responsive UI using React, TypeScript, and Tailwind CSS.
4. Created hands-on simulations to give students practical exposure before choosing a career.

## What we learned
1. AI can revolutionize career counseling by making it dynamic and personalized.
2. Real-time industry analysis is crucial for helping students choose relevant careers.
3. Building a seamless AI-driven platform requires balancing multiple technologies efficiently.
4. User engagement is key—students need interactive, hands-on experiences to make informed decisions.

## What's next for Career Compass AI
1. Expanding career simulations to cover more industries.
2. Enhancing AI recommendations with deeper machine learning insights.
3. Adding mentorship and networking features to connect students with professionals.
4. Launching a mobile app for greater accessibility.
5. Implementing gamification and AI-driven career paths to make learning fun and immersive.

Career Compass AI is just the beginning! We’re redefining career exploration with AI-powered insights, real-time trend analysis, and interactive simulations. The future of career guidance starts here!
