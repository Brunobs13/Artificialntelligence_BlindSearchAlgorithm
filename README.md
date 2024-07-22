[ProblemToSolve.pdf](https://github.com/user-attachments/files/16331841/ProblemToSolve.pdf) - Downloadable file with the problem instructions. 


# Artificial Intelligence Blind Search Algorithm

## Description

This repository contains the solution for a project in the Artificial Intelligence course, focused on protecting the maximum number of families in certain areas against criminal activity using a blind search algorithm.

## Project Structure

This project includes the following files:
- `fullcode.py`: The main Python script implementing the blind search algorithm.
- `Excel Relatório IIA 2201529 EfolioA.xlsx`: Excel report file.
- `Relatório escrito.pdf`: Detailed written report.

## Instructions for Running the Code

### Prerequisites

Ensure you have Python installed on your system. The project was developed using Python 3.x.

### Running the Python Code

To run the Python code, navigate to the directory containing the files and execute the following command:

```bash
python fullcode.py
Make sure that all files are in the same directory.
```

### Project Report

###Introduction

This project aims to protect the maximum number of families in certain areas against criminal activity. We have a budget available for each set of maps (territories) divided into MxN equal parts.

### Algorithms Used

For this exercise, two algorithms were tested:

Breadth-First Search with Depth Limit
Depth-First Search with Depth Limit

Due to the nature of the problem, these algorithms were chosen over others studied so far. Testing revealed that an unbounded search results in an infinite loop consuming significant computer memory, leading to resource exhaustion without yielding a solution.

## Implementation Details

- **Budget Combinations**: A dictionary was created to store possible budget combinations based on the given constraints.
- **Map Dimensions**: Limits were established to ensure that police stations do not extend beyond the map dimensions and do not overlap.
- **Performance Comparison**: Depth-limited search outperformed breadth-limited search in terms of state expansions and execution time, particularly evident in larger instances.

# Results and Analysis

- **Depth-Limited Search:** Efficiently found solutions within the given depth limit.
- **Breadth-Limited Search:** Generated more states and took longer to execute compared to depth-limited search.

## Performance Metrics

Execution time was a key indicator of performance, with depth-limited search showing clear advantages in larger instances.

## Conclusion

The depth-limited search algorithm proved to be more effective for this problem, offering a balance between depth exploration and state expansion. The written report provides a detailed analysis of the algorithms' performance and implementation.
