#pragma once

// enum class of process state
enum class ProcState {NEW, READY, RUNNING, WAITING, TERMINATED};
const int SIZE=30;

class PCB {
 public:

  unsigned int id; //PCB ID 

  unsigned int priority; //Generated priority 1-50

  ProcState state;    //process in the ReadyQueue should be ready

  PCB(); //contsructor.
  PCB(unsigned int,unsigned int);
  ~PCB(); //deconst.

  void display();
  int add_RQ;     //shows the times the PCB has been added and removed from the Queue
  int remove_RQ;  //Included
};

class PCBTable {
 private:
  int Front,Rear,Count; //Front,Rear,Count  ---->  indexes od the table


 public:
  PCBTable();   //contsructor
  ~PCBTable();  //decont.
  
  //array of PCBs
  PCB table[SIZE];

  //mentioned in cpp
  void PCBdisplay();
  void addPCB(PCB);
  bool isEmpty();
  int  TableSize();

};
