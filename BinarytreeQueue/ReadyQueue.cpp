#include "ReadyQueue.h"
#include <iostream>
using namespace std;


ReadyQueue::ReadyQueue(){ //default constructor
  Root=NULL;
}


ReadyQueue::~ReadyQueue(){ //deconstructor
}


//*Add new PCB to the binary tree*
void ReadyQueue::add(PCB* x){  //Pcb --> new PCB
  BSTvertex *N,*V,*Parent;
  Count++;
  x->add_RQ++; 
  x->state=ProcState::READY; //update state of new PCB to READY
  // 1st sets up new vertex
  // N pointing to new vertex 
  N = new BSTvertex;    //New vertex created
  N->L  = NULL;   
  N->R = NULL;   
  N->element = x;     //add element x
  N->Up = NULL;      // no parent for now

  if(Root == NULL){  //if root  = NULL we have a brand new empty tree

  Root = N;         // New vertex adds to root
  }

  else{            // else the tree is not empty
  V = Root;        // start with root v
  Parent = NULL;   // make sure its not pointing elsewhere

  //continuing down the tree
    while (V != NULL){
	      if (N->element->priority < V->element->priority){ 
	        Parent = V; // change Parent to be V to go down
	        V = V->L;  // change V to be V's Left
	      }
	      else{ 
	      
		    Parent = V; // make parent the variable V and go down
		    V = V->R;  // traverse v to the right
	      }
	  }
      
      //if NULL, need to add N as the Parent-child
      
    if (N->element->priority < Parent->element->priority){
	     Parent->L = N;    //Parent's Lc need to point to n
	     N->Up = Parent;   //n needs to look up to parent node
	  }  
    else{
	  Parent->R = N;   //Parent's RC should point to N
	  N->Up = Parent;   //again N must point up to the parent node
    }
  
  }

}

//*traverse through tree recursively to display PCBs in descending order based on priority*

void ReadyQueue::PostOrderTraverse(BSTvertex *x){  //*x is =  to the vertex root
  if (x!= NULL){
    PostOrderTraverse(x->R); // traverse right (recursively)
    x->element->display();
    PostOrderTraverse(x->L);// traverse left   (recursiveley)
  }
}


//*ReadyQueue removes the PCB with largest priority 1-50 from the ReadyQueue returning the pcb that is removed.*

PCB* ReadyQueue::removeHighest(){
  //if the Queue is not empty keep removing the highest PCB
  if(Root!=NULL){
      BSTvertex* dummyNode=NULL; //temporary values to make right child NULL
      BSTvertex* Parent=NULL;
      BSTvertex* V=Root;
      
      if(Count==1)   //If there only one PCB in ReadyQueue
	    Root=dummyNode;  //root = dummyNode
  
      else{  //There is more than one PCB in ReadyQueuev
	      while(V->R){  //Keep looping until V reaches higheet PCB priority
	        Parent=V;
	        V=V->R;
	      }
	  //If the Root PCB has highest priority in ReadyQueue
	      if(V==Root)
	      Root=Root->L;
	  //Root PCB does not have highest priority in ReadyQueue
	      else{
	      if(V->L) //Highest priority PCB has a left child now child is right child to Parent node
		    Parent->R=V->L;
	      else  //else Parent right child is NULL
		    Parent->R=dummyNode;
	    }
	   }
      Count--;
      V->element->remove_RQ++; //Running state pointer updated
      V->element->state=ProcState::RUNNING;  
      return V->element; //return removed PCB 
    }
  //if ReadyQueue == empty nothing return NULL
  return NULL;
}

// *Function returns number of PCBs in ReadyQueue*
int ReadyQueue::size(){return Count;}


//*Prints everything Id,Priority,State. RecursivelyCalls Posr-order-traverse, passing the root nodes
void ReadyQueue::display(){
  cout<<"ID\tPriority\tState"<<endl;
  cout<<"--------------------------"<<endl;
  PostOrderTraverse(Root); //recursive bst call
}

//names 
void ReadyQueue::Marcus_Andre(){
  cout << "Names: Marcus Cook & Andre Castillo\n";
  cout << "-----------------------------------------\n";
  cout<< "Date Written: 2/14/21\n";
  cout << "-----------------------------------------\n";
  cout <<"Course Number: CS 433\n";
  cout << "-----------------------------------------\n";
  cout << "Program description:" << "\n" << "-----------------------------------------\n" << "Ready Queue Data Structure In Which Implements A Process Control Block Maneuvering Within Priorties. The ReadyQueue Consists of a BST (linked list).\n";                 
  cout << "-----------------------------------------\n";
}


