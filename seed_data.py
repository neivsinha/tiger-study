"""
Seed script for Princeton Study Group Finder
Populates the database with Princeton courses and sample study groups
"""
from app import app
from models import db, Course, StudyGroup, Participant
from datetime import datetime, timedelta
import random


def clear_database():
    """Clear all existing data from the database"""
    print("Clearing existing data...")
    with app.app_context():
        Participant.query.delete()
        StudyGroup.query.delete()
        Course.query.delete()
        db.session.commit()
    print("Database cleared!")


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


def seed_study_groups():
    """Seed sample study groups"""
    print("\nSeeding study groups...")

    # Sample participant names
    participant_names = [
        'Alex Chen', 'Sarah Johnson', 'Michael Brown', 'Emily Davis',
        'James Wilson', 'Jessica Martinez', 'David Lee', 'Ashley Garcia',
        'Christopher Rodriguez', 'Amanda Taylor', 'Matthew Anderson',
        'Jennifer Thomas', 'Joshua Jackson', 'Michelle White', 'Andrew Harris'
    ]

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

                # Random host
                host = random.choice(participant_names)

                study_group = StudyGroup(
                    course_id=course.id,
                    title=title,
                    description=description,
                    date_time=meeting_date,
                    location=location,
                    max_participants=max_participants,
                    host_name=host
                )

                db.session.add(study_group)
                db.session.flush()  # Get the ID

                # Add host as first participant
                host_participant = Participant(
                    study_group_id=study_group.id,
                    name=host,
                    joined_at=study_group.created_at
                )
                db.session.add(host_participant)

                # Add 1-4 additional random participants (but not more than capacity)
                if max_participants != -1:
                    num_additional = random.randint(1, min(4, max_participants - 1))
                else:
                    num_additional = random.randint(1, 4)

                available_names = [n for n in participant_names if n != host]
                for j in range(num_additional):
                    if available_names:
                        participant_name = random.choice(available_names)
                        available_names.remove(participant_name)

                        participant = Participant(
                            study_group_id=study_group.id,
                            name=participant_name,
                            joined_at=study_group.created_at + timedelta(hours=random.randint(1, 48))
                        )
                        db.session.add(participant)

                print(f"  Added: {course.code} - {title} ({study_group.participant_count()} participants)")

        db.session.commit()
    print("Successfully seeded study groups!")


def main():
    """Main seeding function"""
    print("="*60)
    print("Princeton Study Group Finder - Database Seeding")
    print("="*60)

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

    # Clear existing data
    clear_database()

    # Seed data
    seed_courses()
    seed_study_groups()

    print("\n" + "="*60)
    print("Database seeding completed successfully!")
    print("="*60)
    print("\nYou can now run the application with: python app.py")


if __name__ == '__main__':
    main()
