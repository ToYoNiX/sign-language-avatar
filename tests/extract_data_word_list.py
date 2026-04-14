"""
Script to extract SigML filenames and save them in various formats.

Usage:
    python script.py -s <source_directory> -o <output_directory> -a <action>

Arguments:
    -s, --source    : Path to the source directory containing .sigml files.
    -o, --output    : Path to the output directory where results will be saved.
    -a, --action    : Action to perform, choose from:
                      - "all": Save all outputs (wordlist, categories, statistics, JSON).
                      - "wordlist": Save extracted filenames in CSV.
                      - "categories": Save category names in CSV.
                      - "statistics": Save word count statistics per category in CSV.
                      - "json": Save a flat words list in JSON.

Example:
    python script.py -s ./data -o ./output -a all
"""
import os
import csv
import json
import argparse


class FileExtractor:
    def __init__(self, base_dir, out_dir):
        self.base_dir = base_dir
        self.out_dir = out_dir
        self.wordlist_file = os.path.join(self.out_dir, "wordlist.csv")
        self.categories_file = os.path.join(self.out_dir, "categories.csv")
        self.stats_file = os.path.join(self.out_dir, "statistics.csv")
        self.json_file = os.path.join(self.out_dir, "categories_files.json")
        self.wordlist = []
        self.categories = set()
        self.category_counts = {}
        self.words = set()

    def extract_file_names(self):
        for root, _, files in os.walk(self.base_dir):
            rel = os.path.relpath(root, self.base_dir)
            category = rel if rel != "." else "uncategorized"
            local_count = 0
            for file in files:
                file_name, ext = os.path.splitext(file)
                if ext.lower() != ".sigml":
                    continue
                self.wordlist.append((file_name, category))
                self.words.add(file_name)
                local_count += 1
            if local_count > 0:
                self.categories.add(category)
                self.category_counts[category] = self.category_counts.get(category, 0) + local_count

    def save_wordlist(self):
        with open(self.wordlist_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["File Name", "Category"])
            writer.writerows(self.wordlist)

    def save_categories(self):
        with open(self.categories_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Category"])
            for category in sorted(self.categories):
                writer.writerow([category])

    def save_statistics(self):
        with open(self.stats_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Word Count"])
            for category, count in sorted(self.category_counts.items()):
                writer.writerow([category, count])

    def save_json(self):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(sorted(self.words), f, indent=2, ensure_ascii=False)

    def run(self, action):
        self.extract_file_names()
        if action == "all":
            self.save_wordlist()
            self.save_categories()
            self.save_statistics()
            self.save_json()
        elif action == "wordlist":
            self.save_wordlist()
        elif action == "categories":
            self.save_categories()
        elif action == "statistics":
            self.save_statistics()
        elif action == "json":
            self.save_json()
        print("Extraction completed!")


def parse_args():
    parser = argparse.ArgumentParser(description="Extract filenames and save in various formats.")
    parser.add_argument("-s", "--source", type=str, required=True, help="Path to the source directory")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to the output directory")
    parser.add_argument("-a", "--action", choices=["all", "wordlist", "categories", "statistics", "json"],
                        required=False, default="all",
                        help="Action to perform: save all, wordlist, categories, statistics, or json")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    extractor = FileExtractor(args.source, args.output)
    extractor.run(args.action)
