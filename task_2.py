import requests
import matplotlib.pyplot as plt
import numpy as np

class StudentScores:
    def __init__(self, url=None):
        self.url = url or "https://api.jsonserve.com/student-scores"

    def get_scores(self):
        try:
            res = requests.get(self.url, timeout=10)
            res.raise_for_status()
            data = res.json()
            print(f"Loaded scores for {len(data)} students")
            return data
        except requests.RequestException:
            print("Could not reach API, using sample data")
            return self.sample_data()

    def sample_data(self):
        return [
            {"name": "Alice Johnson", "math": 85, "science": 92, "english": 88},
            {"name": "Bob Smith", "math": 78, "science": 85, "english": 90},
            {"name": "Carol Williams", "math": 92, "science": 88, "english": 85},
            {"name": "David Brown", "math": 88, "science": 90, "english": 87},
            {"name": "Emma Davis", "math": 95, "science": 93, "english": 91},
            {"name": "Frank Miller", "math": 72, "science": 78, "english": 82},
            {"name": "Grace Wilson", "math": 89, "science": 86, "english": 90},
            {"name": "Henry Moore", "math": 81, "science": 84, "english": 79},
            {"name": "Iris Taylor", "math": 90, "science": 91, "english": 88},
            {"name": "Jack Anderson", "math": 76, "science": 80, "english": 85}
        ]

    def compute_averages(self, students):
        student_avg = {}
        subject_totals = {}

        for student in students:
            subjects = [k for k in student if k != "name"]
            scores = [student[s] for s in subjects]
            student_avg[student["name"]] = sum(scores) / len(scores)

            for subject in subjects:
                subject_totals.setdefault(subject, []).append(student[subject])

        subject_avg = {
            subject: sum(scores) / len(scores)
            for subject, scores in subject_totals.items()
        }

        return student_avg, subject_avg

    def print_summary(self, student_avg, subject_avg):
        print("\n" + "=" * 50)
        print("Student Performance Summary")
        print("=" * 50)

        print("\nTop Students:")
        for i, (name, avg) in enumerate(
            sorted(student_avg.items(), key=lambda x: x[1], reverse=True)[:5], 1
        ):
            print(f"{i}. {name} — {avg:.2f}")

        print("\nSubject Averages:")
        for subject, avg in subject_avg.items():
            print(f"{subject.capitalize()}: {avg:.2f}")

        class_avg = np.mean(list(student_avg.values()))
        print(f"\nClass Average: {class_avg:.2f}")
        print("=" * 50 + "\n")

    def visualize(self, student_avg, subject_avg, students):
        fig, axes = plt.subplots(2, 2, figsize=(15, 11))
        fig.suptitle("Student Score Analysis", fontsize=16)

        names = list(student_avg.keys())
        averages = list(student_avg.values())

        axes[0, 0].bar(names, averages)
        axes[0, 0].set_title("Average Score per Student")
        axes[0, 0].tick_params(axis="x", rotation=45)

        axes[0, 1].bar(subject_avg.keys(), subject_avg.values())
        axes[0, 1].set_title("Average Score per Subject")

        all_scores = [
            score for student in students
            for key, score in student.items()
            if key != "name"
        ]
        axes[1, 0].hist(all_scores, bins=15)
        axes[1, 0].set_title("Score Distribution")

        x = np.arange(len(names))
        width = 0.25
        for i, subject in enumerate(subject_avg):
            subject_scores = [s[subject] for s in students]
            axes[1, 1].bar(x + i * width, subject_scores, width, label=subject)

        axes[1, 1].set_xticks(x + width)
        axes[1, 1].set_xticklabels([n.split()[0] for n in names], rotation=45)
        axes[1, 1].set_title("Subject Scores by Student")
        axes[1, 1].legend()

        plt.tight_layout()
        plt.savefig("student_scores_analysis.png")
        plt.show()


def main():
    analyzer = StudentScores()
    students = analyzer.get_scores()
    student_avg, subject_avg = analyzer.compute_averages(students)
    analyzer.print_summary(student_avg, subject_avg)
    analyzer.visualize(student_avg, subject_avg, students)


if __name__ == "__main__":
    main()
