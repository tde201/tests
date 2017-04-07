# -*- coding: utf-8 -*-
"""
Script to answer questions 1 and 2 of Algorithms II week 1 programming task.
"""

def read_jobs_file(fileName):
    """ Read in the contentsof the <jobs.txt> file.
    
    The format is assumed to be an integer on line 0 indicating the number of jobs. Then
    each following row has a tuple of the job weight and the job length separated by a space.
    The job weight and h=job length are assumed to be integers.
    
    Args:
      fileName: The name of the file to open in this format.
      
    Returns:
      numOfJobs: Integer. The number of jobs in the file.
      jobsList: List of integer tuples. This lists the jobs in order. Each tuple describes the
                weight, the job length, the difference in weight and job length, as well as the
                ratio of weight to job length.
    """
    jobsList = list()
    
    with open(fileName, 'r') as jobsFile:
        for lineNum, line in enumerate(jobsFile):
            row = line.strip('\n')
            if lineNum == 0:
                numOfJobs = int(row)
            else:
                (weight, length) = row.split(' ')
                difference = int(weight) - int(length)
                ratio = float(weight) / float(length)
                jobsList.append((int(weight), int(length), difference, ratio))
                
    return numOfJobs, jobsList

def greedy1(jobsList):
    """ Schedule jobs in decreasing order of (weight - length), breaking ties by scheduling
    jobs with the highest weight first.
    
    This algorithm is not optimal in all cases!
    
    Args:
      jobsList: List of integer tuples. This list the jobs in order. Each tuple describes the
                weight, the job length, the difference in weight and job length, as well as the
                ratio of weight to job length.
                
    Returns:
      sumOfWeightedCompletionTimes: Integer. The sum of the weighted completion times.
    """
    # Sort by weight in reverse order
    jobsList.sort(key = lambda tup: tup[0], reverse = True)
    
    # Sort by difference in weight and length
    jobsList.sort(key = lambda tup: tup[2], reverse = True)
    
    jobLengths = [x[1] for x in jobsList]
    jobWeights = [x[0] for x in jobsList]
    completionTimes = [sum(jobLengths[:i + 1]) for i, x in enumerate(jobLengths)]
    sumOfWeightedCompletionTimes = dot(jobWeights, completionTimes)
    
    return sumOfWeightedCompletionTimes

def greedy2(jobsList):
    """ Schedule jobs in decreasing order of (weight/length), breaking ties by scheduling
    jobs with the highest weight first.
    
    This algorithm is optimal in all cases!
    
    Args:
      jobsList: List of integer tuples. This list the jobs in order. Each tuple describes the
                weight, the job length, the difference in weight and job length, as well as the
                ratio of weight to job length.
                
    Returns:
      sumOfWeightedCompletionTimes: Integer. The sum of the weighted completion times.
    """
    # Sort by ratio of weight/length
    jobsList.sort(key = lambda tup: tup[3], reverse = True)
    
    jobLengths = [x[1] for x in jobsList]
    jobWeights = [x[0] for x in jobsList]
    completionTimes = [sum(jobLengths[:i + 1]) for i, x in enumerate(jobLengths)]
    sumOfWeightedCompletionTimes = dot(jobWeights, completionTimes)
    
    return sumOfWeightedCompletionTimes, jobWeights, completionTimes

def dot(a, b):
    """ Find sum of product of two arrays a and b.
    
    Args:
      a: An integer array of length n.
      b: An integer array of length n.
      
    Returns:
      sumProduct: The sum of the product of the elements of a and b.
    """
    product = list()
    n = len(a)
    assert(n == len(b))
    for i in range(n):
        product.append(a[i] * b[i])
        
    sumProduct = sum(product)
    
    return sumProduct

if __name__ == "__main__":
    fileName = 'jobs.txt'
    numOfJobs, jobsList = read_jobs_file(fileName)
    output1 = greedy1(jobsList)
    output2, jobWeights, completionTimes = greedy2(jobsList)
    print output1, output2, output1 >= output2