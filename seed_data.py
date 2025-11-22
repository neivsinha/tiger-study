"""
Seed script for Princeton Study Group Finder
Populates the database with Princeton courses and sample study groups
"""
from app import app
from models import db, User, Course, StudyGroup, Participant, DiscussionPost, DiscussionReply, PostVote, ReplyVote
from datetime import datetime, timedelta
import random


def clear_database():
    """Clear all existing data from the database"""
    print("Clearing existing data...")
    with app.app_context():
        ReplyVote.query.delete()
        PostVote.query.delete()
        DiscussionReply.query.delete()
        DiscussionPost.query.delete()
        Participant.query.delete()
        StudyGroup.query.delete()
        Course.query.delete()
        User.query.delete()
        db.session.commit()
    print("Database cleared!")


def seed_users():
    """Seed sample Princeton users"""
    print("\nSeeding users...")

    users_data = [
        {'email': 'jsmith26@princeton.edu', 'username': 'jsmith26',
         'full_name': 'John Smith', 'class_year': 2026, 'password': 'password123'},
        {'email': 'alee27@princeton.edu', 'username': 'alee27',
         'full_name': 'Alice Lee', 'class_year': 2027, 'password': 'password123'},
        {'email': 'mbrown25@princeton.edu', 'username': 'mbrown25',
         'full_name': 'Michael Brown', 'class_year': 2025, 'password': 'password123'},
        {'email': 'sjohnson28@princeton.edu', 'username': 'sjohnson28',
         'full_name': 'Sarah Johnson', 'class_year': 2028, 'password': 'password123'},
        {'email': 'dchen26@princeton.edu', 'username': 'dchen26',
         'full_name': 'David Chen', 'class_year': 2026, 'password': 'password123'},
        {'email': 'ewilliams27@princeton.edu', 'username': 'ewilliams27',
         'full_name': 'Emily Williams', 'class_year': 2027, 'password': 'password123'},
        {'email': 'rgarcia25@princeton.edu', 'username': 'rgarcia25',
         'full_name': 'Robert Garcia', 'class_year': 2025, 'password': 'password123'},
        {'email': 'lmartinez26@princeton.edu', 'username': 'lmartinez26',
         'full_name': 'Laura Martinez', 'class_year': 2026, 'password': 'password123'},
    ]

    users = []
    for user_data in users_data:
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            full_name=user_data['full_name'],
            class_year=user_data['class_year']
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print(f"  Created {len(users)} users")
    return users


def seed_courses():
    """Seed Princeton courses"""
    print("\nSeeding courses...")

    courses_data = [
        {
            'code': 'COS126',
            'title': 'Computer Science: An Interdisciplinary Approach',
            'description': 'Introduction to computer science and programming. Core principles of computing and their applications in various fields.'
        },
        {
            'code': 'COS226',
            'title': 'Algorithms and Data Structures',
            'description': 'Study of algorithms, data structures, and their implementation and application in problem solving.'
        },
        {
            'code': 'MAT201',
            'title': 'Multivariable Calculus',
            'description': 'Vector algebra and geometry, partial derivatives, multiple integrals, line and surface integrals.'
        },
        {
            'code': 'MAT202',
            'title': 'Linear Algebra with Applications',
            'description': 'Systems of linear equations, matrix operations, vector spaces, eigenvalues and eigenvectors.'
        },
        {
            'code': 'PHY103',
            'title': 'General Physics I',
            'description': 'Mechanics, wave motion, kinetic theory, and thermodynamics with applications to the natural sciences.'
        },
        {
            'code': 'PHY104',
            'title': 'General Physics II',
            'description': 'Electricity, magnetism, electromagnetic waves, optics, and selected topics in modern physics.'
        },
        {
            'code': 'ECO100',
            'title': 'Introduction to Microeconomics',
            'description': 'Study of individual decision-making, market mechanisms, and resource allocation in modern economies.'
        },
        {
            'code': 'ECO101',
            'title': 'Introduction to Macroeconomics',
            'description': 'Analysis of aggregate economic activity, including national income, employment, inflation, and economic growth.'
        },
        {
            'code': 'CHM201',
            'title': 'General Chemistry',
            'description': 'Fundamental principles of chemistry including atomic structure, bonding, thermodynamics, and kinetics.'
        },
        {
            'code': 'MOL214',
            'title': 'Introduction to Cellular and Molecular Biology',
            'description': 'Modern biology focusing on cellular structure, function, and molecular mechanisms of life.'
        },
        {
            'code': 'ORF245',
            'title': 'Fundamentals of Statistics',
            'description': 'Introduction to statistical thinking and data analysis with applications across disciplines.'
        },
        {
            'code': 'PSY101',
            'title': 'Introduction to Psychology',
            'description': 'Survey of scientific study of mind and behavior including cognition, development, and social psychology.'
        },
        {
            'code': 'COS217',
            'title': 'Introduction to Programming Systems',
            'description': 'Study of programming in C and assembly language, operating systems concepts, and system-level programming.'
        },
        {
            'code': 'EGR154',
            'title': 'Introduction to Engineering',
            'description': 'Introduction to engineering design process through hands-on projects and interdisciplinary collaboration.'
        },
        {
            'code': 'HIS210',
            'title': 'The World Since 1945',
            'description': 'Examination of major global developments from the end of World War II to the present.'
        }
    ]

    with app.app_context():
        for course_data in courses_data:
            course = Course(**course_data)
            db.session.add(course)
            print(f"  Added: {course.code} - {course.title}")

        db.session.commit()
    print(f"Successfully seeded {len(courses_data)} courses!")


def seed_study_groups(users):
    """Seed sample study groups"""
    print("\nSeeding study groups...")

    # Get all users for random assignment
    if not users:
        users = User.query.all()

    if len(users) < 2:
        print("  Warning: Not enough users to create study groups properly")
        return

    # Sample locations
    locations = [
        'Fine Hall 214',
        'Frist Campus Center, 3rd Floor',
        'Lewis Library Study Room 3A',
        'Friend Center 101',
        'McCosh Hall 50',
        'Firestone Library, Room B-2',
        'Virtual/Zoom',
        'Butler College Study Room',
        'Whitman College Commons',
        'Chancellor Green Library',
        'Engineering Quad, Room E-Quad C205'
    ]

    # Study group templates for different courses
    study_group_templates = {
        'COS126': [
            ('Midterm Review Session', 'Going over key concepts for the upcoming midterm. Bring questions!'),
            ('Problem Set 3 Help', 'Working through recursion problems together. Let\'s tackle the challenging questions.'),
            ('Arrays and Loops Practice', 'Practice session focused on array manipulation and loop constructs.'),
            ('Final Exam Prep', 'Comprehensive review covering all course material. Great for final prep!'),
        ],
        'COS226': [
            ('Graph Algorithms Study', 'Deep dive into graph algorithms including DFS, BFS, and shortest paths.'),
            ('Binary Search Trees Workshop', 'Working through BST implementations and balancing techniques.'),
            ('Sorting Algorithms Review', 'Comparing different sorting algorithms and their time complexities.'),
        ],
        'MAT201': [
            ('Multiple Integrals Practice', 'Working through double and triple integral problems from the textbook.'),
            ('Vector Calculus Study Session', 'Reviewing gradient, divergence, and curl applications.'),
            ('Midterm Prep - Partial Derivatives', 'Focus on partial derivatives and applications to optimization.'),
        ],
        'MAT202': [
            ('Linear Transformations Workshop', 'Understanding linear transformations and matrix representations.'),
            ('Eigenvalue Problems Study Group', 'Working through eigenvalue and eigenvector problems together.'),
            ('Final Review Session', 'Comprehensive review of all linear algebra topics covered this semester.'),
        ],
        'PHY103': [
            ('Mechanics Problem Solving', 'Working through challenging mechanics problems from recent problem sets.'),
            ('Lab Report Help Session', 'Get help formatting and analyzing your lab reports.'),
            ('Kinematics and Dynamics Review', 'Review of motion equations and Newton\'s laws with practice problems.'),
        ],
        'PHY104': [
            ('Electricity and Magnetism Study', 'Working through E&M concepts including Gauss\'s law and circuits.'),
            ('Optics and Waves Review', 'Discussion of wave properties, interference, and diffraction.'),
        ],
        'ECO100': [
            ('Supply and Demand Analysis', 'Practice with supply/demand curves and market equilibrium problems.'),
            ('Consumer Theory Study Group', 'Working through utility functions and consumer optimization.'),
            ('Game Theory Problems', 'Solving game theory problems and Nash equilibrium applications.'),
        ],
        'ECO101': [
            ('Macro Models Review', 'Discussing IS-LM model, AD-AS framework, and policy implications.'),
            ('GDP and National Accounts', 'Working through national income accounting and GDP calculations.'),
        ],
        'CHM201': [
            ('Thermodynamics Problem Session', 'Solving thermodynamics problems including enthalpy and entropy.'),
            ('Organic Chemistry Basics', 'Introduction to organic compounds and nomenclature.'),
            ('Lab Practical Prep', 'Preparing for the upcoming lab practical with technique review.'),
        ],
        'MOL214': [
            ('Cell Biology Review', 'Discussion of cell structure, organelles, and cellular processes.'),
            ('DNA Replication and Transcription', 'Deep dive into molecular mechanisms of gene expression.'),
            ('Midterm Study Marathon', 'Intensive review session covering all topics for the midterm.'),
        ],
        'ORF245': [
            ('Hypothesis Testing Workshop', 'Working through hypothesis testing problems and p-values.'),
            ('Probability Distributions Study', 'Review of normal, binomial, and other key distributions.'),
            ('R Programming Help', 'Get help with R coding for your statistics assignments.'),
        ],
        'PSY101': [
            ('Cognitive Psychology Discussion', 'Exploring memory, attention, and decision-making research.'),
            ('Developmental Psych Review', 'Discussing theories of cognitive and social development.'),
            ('Research Methods Study Group', 'Understanding experimental design and statistical analysis in psychology.'),
        ]
    }

    with app.app_context():
        courses = Course.query.all()

        for course in courses:
            # Get templates for this course, or use generic ones
            if course.code in study_group_templates:
                templates = study_group_templates[course.code]
            else:
                templates = [
                    ('Study Session', 'General study session for course material.'),
                    ('Problem Set Help', 'Working through problem sets together.'),
                ]

            # Create 2-4 study groups per course
            num_groups = random.randint(2, 4)

            for i in range(min(num_groups, len(templates))):
                title, description = templates[i]

                # Random date/time in the future or past
                days_offset = random.randint(-7, 21)  # Some past, mostly future
                hour = random.choice([10, 13, 14, 15, 16, 18, 19, 20])
                minute = random.choice([0, 30])

                meeting_date = datetime.now() + timedelta(days=days_offset, hours=hour-datetime.now().hour, minutes=minute-datetime.now().minute)

                # Random location
                location = random.choice(locations)

                # Random capacity
                max_participants = random.choice([4, 5, 6, 8, 10, -1])

                # Random host from users
                host_user = random.choice(users)

                study_group = StudyGroup(
                    course_id=course.id,
                    host_id=host_user.id,
                    title=title,
                    description=description,
                    date_time=meeting_date,
                    location=location,
                    max_participants=max_participants
                )

                db.session.add(study_group)
                db.session.flush()  # Get the ID

                # Add host as first participant
                host_participant = Participant(
                    study_group_id=study_group.id,
                    user_id=host_user.id,
                    joined_at=study_group.created_at
                )
                db.session.add(host_participant)

                # Add 1-4 additional random participants (but not more than capacity)
                if max_participants != -1:
                    num_additional = random.randint(1, min(4, max_participants - 1))
                else:
                    num_additional = random.randint(1, 4)

                available_users = [u for u in users if u.id != host_user.id]
                added_participants = set([host_user.id])

                for j in range(num_additional):
                    if available_users:
                        participant_user = random.choice(available_users)
                        if participant_user.id not in added_participants:
                            added_participants.add(participant_user.id)

                            participant = Participant(
                                study_group_id=study_group.id,
                                user_id=participant_user.id,
                                joined_at=study_group.created_at + timedelta(hours=random.randint(1, 48))
                            )
                        db.session.add(participant)

                print(f"  Added: {course.code} - {title} ({study_group.participant_count()} participants)")

        db.session.commit()
    print("Successfully seeded study groups!")


def seed_discussions(users):
    """Seed sample discussion posts and replies"""
    print("\nSeeding discussion posts...")

    # Get all users for random assignment
    if not users:
        users = User.query.all()

    if len(users) < 2:
        print("  Warning: Not enough users to create discussions properly")
        return

    # Sample author names (no longer needed, keeping for structure)
    author_names_deprecated = [
        'Alex Chen', 'Sarah Johnson', 'Michael Brown', 'Emily Davis',
        'James Wilson', 'Jessica Martinez', 'David Lee', 'Ashley Garcia',
        'Christopher Rodriguez', 'Amanda Taylor', 'Matthew Anderson'
    ]

    # Discussion templates by category
    discussion_templates = {
        'COS126': [
            {'title': 'Recursion vs. Iteration - When to Use Each?', 'category': 'Question',
             'content': 'I\'m working on Problem Set 3 and struggling to decide when to use recursion versus iteration. Can someone explain when each approach is better? Specifically for tree traversals and array processing.'},
            {'title': 'Best Resources for Understanding Arrays', 'category': 'Resources',
             'content': 'Found this great visualization tool for understanding array operations: https://visualgo.net\n\nIt really helped me grasp how array indexing works and common operations like insertion and deletion. Highly recommend!'},
            {'title': 'Midterm Study Group Tips', 'category': 'Study Tips',
             'content': 'Just wanted to share what worked for our study group last semester:\n\n1. Review lectures 1-2 days before meeting\n2. Each person presents one challenging problem\n3. Work through past exam problems together\n4. Quiz each other on key concepts\n\nWe all did really well on the midterm using this approach!'},
            {'title': 'Problem Set 4 - Anyone else stuck on the optional challenge?', 'category': 'Question',
             'content': 'The optional challenge about optimizing the search algorithm is really tough. I\'ve tried a few approaches but my solution is still too slow. Has anyone made progress on this?'},
        ],
        'COS226': [
            {'title': 'Graph Algorithms - DFS vs BFS Clarification', 'category': 'Question',
             'content': 'Can someone help clarify when to use DFS versus BFS? I understand the mechanics of each, but I\'m not clear on which one is better for different use cases.'},
            {'title': 'Amazing Visualization for BST Operations', 'category': 'Resources',
             'content': 'Check out this interactive BST visualizer I found. You can see rotations, insertions, and deletions in real-time: https://www.cs.usfca.edu/~galles/visualization/BST.html'},
            {'title': 'Final Exam Preparation Strategy', 'category': 'Exam Prep',
             'content': 'With the final coming up, what are people focusing on? I\'m planning to:\n- Review all sorting algorithms and their complexities\n- Practice graph problems\n- Go through priority queues again\n\nWhat else should be on this list?'},
        ],
        'MAT201': [
            {'title': 'Double Integrals Order of Integration', 'category': 'Question',
             'content': 'I keep getting confused about when to switch the order of integration. Is there a systematic way to determine the best order? Sometimes one order seems much easier than the other.'},
            {'title': 'Vector Calculus Study Resources', 'category': 'Resources',
             'content': 'Paul\'s Online Math Notes have been a lifesaver for this class: http://tutorial.math.lamar.edu\n\nThe practice problems are great and the explanations are clearer than the textbook sometimes.'},
            {'title': 'Partial Derivatives - Common Mistakes to Avoid', 'category': 'Study Tips',
             'content': 'After tutoring for this class, here are the most common mistakes I see:\n\n1. Forgetting to apply chain rule\n2. Not treating other variables as constants\n3. Sign errors when taking second derivatives\n4. Mixing up the order of mixed partials\n\nDouble-check these when solving problems!'},
        ],
        'ECO100': [
            {'title': 'Elasticity Calculations - Need Help', 'category': 'Question',
             'content': 'I understand the concept of price elasticity, but I\'m struggling with the calculations. Especially when we need to determine if demand is elastic or inelastic. Can someone walk through an example?'},
            {'title': 'Game Theory Practice Problems', 'category': 'Resources',
             'content': 'Found a great set of game theory practice problems with solutions. Really helped me prepare for the midterm. DM me if you want the link!'},
            {'title': 'Understanding Supply and Demand Shifts', 'category': 'Study Tips',
             'content': 'Tip: Draw the graphs! I used to try to visualize shifts in my head but drawing them out makes it SO much clearer. Also helps on exams when you can sketch quick diagrams.'},
        ],
        'PHY103': [
            {'title': 'Kinematics Problem Solving Approach', 'category': 'Study Tips',
             'content': 'Here\'s my systematic approach that\'s been working:\n\n1. Draw a diagram with coordinate system\n2. List known and unknown variables\n3. Choose the right kinematic equation\n4. Solve algebraically before plugging in numbers\n5. Check if the answer makes physical sense\n\nAnyone else have tips to add?'},
            {'title': 'Lab Report Format Question', 'category': 'Question',
             'content': 'For the uncertainty analysis section, should we include both systematic and random errors? The rubric isn\'t super clear on this.'},
        ],
        'PSY101': [
            {'title': 'Memory Techniques for Course Material', 'category': 'Study Tips',
             'content': 'Ironically, using memory techniques from the course to learn course material! \n\nI\'ve been using:\n- Spaced repetition for definitions\n- Method of loci for studies/researchers\n- Chunking for related concepts\n\nIt\'s actually working pretty well!'},
            {'title': 'Development Psychology Resources', 'category': 'Resources',
             'content': 'The Khan Academy psychology section has great videos that complement our textbook. The animations really help visualize concepts like Piaget\'s stages.'},
        ]
    }

    # Reply templates
    reply_templates = [
        "This is really helpful, thanks for sharing!",
        "I was wondering the same thing. Following this thread!",
        "Great explanation! That cleared up my confusion.",
        "Adding to this - I found that practicing similar problems really helps.",
        "Thanks! This resource is exactly what I needed.",
        "Good question - I think the key is to look at...",
        "I had the same issue. What helped me was...",
        "This makes so much sense now. Appreciate the detailed response!",
        "Definitely agree with this approach. It worked well for me too.",
        "Can you elaborate a bit more on this part?",
    ]

    with app.app_context():
        courses = Course.query.all()

        post_count = 0
        reply_count = 0

        for course in courses:
            # Get templates for this course or skip if none
            if course.code not in discussion_templates:
                continue

            templates = discussion_templates[course.code]

            # Create 3-5 discussion posts per course (or all available if fewer)
            max_posts = min(5, len(templates))
            min_posts = min(3, len(templates))
            num_posts = random.randint(min_posts, max_posts) if min_posts <= max_posts else len(templates)

            for i in range(num_posts):
                template = templates[i]

                # Random creation time (1-30 days ago)
                days_ago = random.randint(1, 30)
                hours_ago = random.randint(0, 23)
                created_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

                # Pin first post sometimes
                pinned = (i == 0 and random.random() < 0.3)

                # Random author from users
                author_user = random.choice(users)

                post = DiscussionPost(
                    course_id=course.id,
                    author_id=author_user.id,
                    title=template['title'],
                    content=template['content'],
                    category=template['category'],
                    pinned=pinned,
                    created_at=created_time
                )

                db.session.add(post)
                db.session.flush()  # Get the post ID

                # Add 0-3 replies to each post
                num_replies = random.randint(0, 3)

                for j in range(num_replies):
                    # Get available reply authors (different from post author)
                    available_reply_users = [u for u in users if u.id != author_user.id]
                    if available_reply_users:
                        reply_user = random.choice(available_reply_users)

                        # Reply created after post
                        reply_hours_offset = random.randint(2, 72)
                        reply_time = created_time + timedelta(hours=reply_hours_offset)

                        reply = DiscussionReply(
                            post_id=post.id,
                            author_id=reply_user.id,
                            content=random.choice(reply_templates),
                            created_at=reply_time
                        )

                        db.session.add(reply)
                        reply_count += 1

                post_count += 1
                print(f"  Added: {course.code} - {template['title'][:50]}... ({num_replies} replies)")

        db.session.commit()
    print(f"Successfully seeded {post_count} discussion posts with {reply_count} replies!")


def seed_votes(users):
    """Seed sample votes on discussion posts and replies"""
    print("\nSeeding votes...")

    # Get all users for voting
    if not users:
        users = User.query.all()

    if len(users) < 2:
        print("  Warning: Not enough users to create votes properly")
        return

    with app.app_context():
        all_posts = DiscussionPost.query.all()
        all_replies = DiscussionReply.query.all()

        post_vote_count = 0
        reply_vote_count = 0

        # Vote on posts
        for post in all_posts:
            # Determine how many users will vote on this post (realistic distribution)
            # Some posts get lots of votes, some get few
            vote_probability = random.random()

            if vote_probability < 0.2:
                # Hot post - lots of votes (60-80% of users)
                num_voters = random.randint(int(len(users) * 0.6), int(len(users) * 0.8))
            elif vote_probability < 0.5:
                # Popular post - moderate votes (30-50% of users)
                num_voters = random.randint(int(len(users) * 0.3), int(len(users) * 0.5))
            else:
                # Regular post - fewer votes (10-30% of users)
                num_voters = random.randint(int(len(users) * 0.1), int(len(users) * 0.3))

            # Select random voters (excluding post author)
            available_voters = [u for u in users if u.id != post.author_id]
            voters = random.sample(available_voters, min(num_voters, len(available_voters)))

            for voter in voters:
                # Vote distribution: 70% upvote, 30% downvote (realistic for helpful content)
                vote_type = 1 if random.random() < 0.7 else -1

                # Create vote with timestamp after post creation
                vote_time = post.created_at + timedelta(hours=random.randint(1, 72))

                post_vote = PostVote(
                    post_id=post.id,
                    user_id=voter.id,
                    vote_type=vote_type,
                    created_at=vote_time
                )
                db.session.add(post_vote)
                post_vote_count += 1

            # Update post score
            post.score = sum(v.vote_type for v in PostVote.query.filter_by(post_id=post.id).all())

        # Vote on replies
        for reply in all_replies:
            # Replies typically get fewer votes than posts
            vote_probability = random.random()

            if vote_probability < 0.15:
                # Great reply - good votes (40-60% of users)
                num_voters = random.randint(int(len(users) * 0.4), int(len(users) * 0.6))
            elif vote_probability < 0.4:
                # Good reply - moderate votes (20-40% of users)
                num_voters = random.randint(int(len(users) * 0.2), int(len(users) * 0.4))
            else:
                # Regular reply - fewer votes (5-20% of users)
                num_voters = random.randint(int(len(users) * 0.05), int(len(users) * 0.2))

            # Select random voters (excluding reply author)
            available_voters = [u for u in users if u.id != reply.author_id]
            if num_voters > len(available_voters):
                num_voters = len(available_voters)

            if num_voters > 0:
                voters = random.sample(available_voters, num_voters)

                for voter in voters:
                    # Vote distribution: 75% upvote, 25% downvote (replies are usually helpful)
                    vote_type = 1 if random.random() < 0.75 else -1

                    # Create vote with timestamp after reply creation
                    vote_time = reply.created_at + timedelta(hours=random.randint(1, 48))

                    reply_vote = ReplyVote(
                        reply_id=reply.id,
                        user_id=voter.id,
                        vote_type=vote_type,
                        created_at=vote_time
                    )
                    db.session.add(reply_vote)
                    reply_vote_count += 1

                # Update reply score
                reply.score = sum(v.vote_type for v in ReplyVote.query.filter_by(reply_id=reply.id).all())

        db.session.commit()
        print(f"  Created {post_vote_count} post votes and {reply_vote_count} reply votes")

        # Print some statistics
        high_score_posts = DiscussionPost.query.filter(DiscussionPost.score >= 3).count()
        low_score_posts = DiscussionPost.query.filter(DiscussionPost.score < 0).count()
        print(f"  High-scoring posts (score >= 3): {high_score_posts}")
        print(f"  Low-scoring posts (score < 0): {low_score_posts}")

    print("Successfully seeded votes!")


def main():
    """Main seeding function"""
    print("="*60)
    print("Princeton Study Group Finder - Database Seeding")
    print("="*60)

    with app.app_context():
        # Drop all tables and recreate with new schema
        print("Dropping all tables...")
        db.drop_all()
        print("Creating fresh tables with new schema...")
        db.create_all()

        # Clear existing data (moved inside context)
        print("Clearing existing data...")
        ReplyVote.query.delete()
        PostVote.query.delete()
        DiscussionReply.query.delete()
        DiscussionPost.query.delete()
        Participant.query.delete()
        StudyGroup.query.delete()
        Course.query.delete()
        User.query.delete()
        db.session.commit()
        print("Database cleared!")

        # Seed data (IMPORTANT: Users FIRST!)
        users = seed_users()
        seed_courses()
        seed_study_groups(users)
        seed_discussions(users)
        seed_votes(users)

    print("\n" + "="*60)
    print("Database seeding completed successfully!")
    print("="*60)
    print("\nYou can now run the application with: python app.py")


if __name__ == '__main__':
    main()
