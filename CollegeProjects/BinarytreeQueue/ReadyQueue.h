#pragma once

#include "PCB.h"

/*
 * ReadyQueue is a queue of PCB's that are in the READY state to be scheduled to run.
 * It should be a priority queue here uch that the process with the highest priority
 * can be selected next.
 */
const int MAX=15;

struct BSTvertex{
  BSTvertex *Up;  // pointing to the parent node in b
  BSTvertex *L;   // Left of bst
  BSTvertex *R;   // Right of bst
  PCB* element;
};

class ReadyQueue {
 private:
  int Count = 0;
  BSTvertex* Root;  


 public:
  //Req. Functions
  ReadyQueue();   //const.
  ~ReadyQueue(); //deconst.
  
  void add(PCB*); //adding process into ready queue.  
  int size();     //Returns number of elements in the queue
  PCB* removeHighest();  //removing the PCB with highest priority from the queue then --> return
  void display();  //Prints the queue contents to standard output.
  void PostOrderTraverse(BSTvertex*);    //Traversing the tree
  void Marcus_Andre();                //prints out names and breif descrip.
};
