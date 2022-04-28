#include "PCB.h"
#include "ReadyQueue.h"
#include <iostream>
using namespace std;


PCB::PCB(){ //constructor default
  priority=0; id=0;
  add_RQ=0; remove_RQ=0;
  state=ProcState::NEW;
}

PCB::~PCB(){  //decons.
}


PCB::PCB(unsigned int IDNum,unsigned int priorityNum){  //PCB overload constructor
  id=IDNum;
  priority=priorityNum;
  state=ProcState::NEW;
  add_RQ=0; remove_RQ=0;
}



void PCB::display(){  //Displays the ID,the Priority and the Running state of the  PCB
  cout<<id;
  cout<<"\t";
  cout <<priority<<"\t\t";  //if statements to find current state of PCB
  
  if(state==ProcState::NEW)          //new state
    cout<<"\t(NEW)"<<endl;
  else if(state==ProcState::READY)   //ready state
    cout<<"\t(READY)"<<endl;
  else if(state==ProcState::RUNNING) //running state
    cout<<"\t(RUNNING)"<<endl;
  else if(state==ProcState::WAITING) //waiting state
    cout<<"\t(WAITING)"<<endl;
  else
    cout<<"\t(TERMINATED)"<<endl;        //else TERMINATED
}  



PCBTable::PCBTable(){ //default const. of pcb table
  Count=0;Front=-1;Rear=-1;
}


PCBTable::~PCBTable(){ //dec. of pcb table
}


bool PCBTable::isEmpty(){
  if(Rear==-1 && Front==-1 && Count==0)  //*if PCB table empty return true, else false*
    return 1;//true
  else
    return 0;//false
}

void PCBTable::PCBdisplay(){ //*Display ID,Priority and the state for each PCB in the table*
  cout<<"ID\tPriority\tState"<<endl;
  cout<<"------------------------------------"<<endl;

  if(!isEmpty())   //if table is empty there is nothing to print :)
    for(int i=0;i<Count;i++)
      table[i].display();
}


void PCBTable::addPCB(PCB newPCB){  //*Add a new PCB to the table*
  if(!isEmpty()){  //if not the first element of the entire list
      Rear++;
      table[Rear]=newPCB;
      Count++;
  }
  else{           //if it is the first ele in the list
      Front++;Rear++;
      table[Front]=newPCB;
      Count++;
  }
}


int PCBTable::TableSize(){return Count;}  //returning the current amount of elements in table



