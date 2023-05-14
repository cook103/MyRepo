//Marcus Cook Jr //cook103@cougars.csusm.edu
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include "ReadyQueue.h"
using namespace std;


int main(){
ReadyQueue Names;
Names.Marcus_Andre();  //call for name prints

cout << "**TEST 1**" << endl;
cout << "==========================================" << endl;
  
PCBTable FirstTable;
  
int i = 0;  
while(i<30){                //1 to 30 entries
    PCB Form_new_PCB(i,i); //id number and priority #
    FirstTable.addPCB(Form_new_PCB);
i++;
}
  
  
ReadyQueue Q1;

Q1.add(&FirstTable.table[15]);  //adding process 15
Q1.add(&FirstTable.table[6]);   //adding process 6
Q1.add(&FirstTable.table[23]);  //adding process 23
Q1.add(&FirstTable.table[29]);  //adding process 29
Q1.add(&FirstTable.table[8]);   //adding process 8
Q1.display();

cout<<endl;

Q1.removeHighest();  //removing the highest priority
Q1.display();        //Display

cout<<endl;

Q1.removeHighest();  //again
Q1.display();

cout<<endl;

Q1.add(&FirstTable.table[3]);   //adding process 3
Q1.add(&FirstTable.table[17]);  //adding process 17
Q1.add(&FirstTable.table[22]);  //adding process 22
Q1.add(&FirstTable.table[12]);  //adding process 12
Q1.add(&FirstTable.table[19]);  //adding process 19
Q1.display();

cout<<endl;


while(Q1.size()!=0){ // if q1 size does not equal zero remove the highest priority and display
    Q1.removeHighest();
    Q1.display();
    cout<<endl;
}

//-------------------------------------------------------------------------------------------

cout << "**TEST 2**" << endl;
cout << "==========================================" << endl;

PCBTable SecondTable;

//PCBTable loop to load new entries
for(int i = 1; i <= 15; i++){  // generating 15 table entries 
    int n_Priority = 0;    //retrieve random priority ranging from 1 - priorityMAX
      while(n_Priority == 0)
	        n_Priority = rand()%(50+1); //max priority randomlly generated is 50
          PCB NewPCB(i,n_Priority);
          SecondTable.addPCB(NewPCB);
    }

  cout<<endl;

//adding and removing from ReadyQueue

ReadyQueue Q2;
PCB* NewPCB=new PCB;

int iterations = 1000000;

for(int i = 0; i < 1000000; i++){  //Million iteration
    int rand_pick = rand()%2;      //randomly generatinf a pick to throw into queue
    if (rand_pick == 0){           //if choice is even remove
	  Q2.removeHighest();
	  }
    else{  //otherwise odd
	  int result;
    result = Q2.size();
    if (result != MAX){    //if Queue is full dont add
	    
	  do{
		    int number=0;
		            //getting a random number between 1 when searching table for PCB table
		while (number==0)
		    number= rand()%(SecondTable.TableSize()+1);
		    NewPCB = &SecondTable.table[number-1];
		   //try again if PCB id was not found in PCBTable or PCB is already inside the Queue 
	   }
        while(NewPCB == NULL || NewPCB->state == ProcState::READY); //after finding PCB add to Queue
	        Q2.add(NewPCB);
	    }
	  }
  }
  
  clock_t APT; //approximate processor time   ==  (APT)
  APT = clock(); 
  cout << "Total Run Time: " << endl;
  cout << "APT ==(" << (float)(APT)/CLOCKS_PER_SEC << " seconds)" << endl;
  cout << endl;
  

  Q2.display(); //display ready queue
  cout << endl;

  int j = 1;  //want to start from 1 = 1-15
  int added,removed;
  added = SecondTable.table[j-1].add_RQ ; //how many times Added
  removed = SecondTable.table[j-1].remove_RQ;
  while(j <= SecondTable.TableSize()){ //Loop displays how many times the PCB adds and removes
      cout<< "PCB ID " << j; 
      cout<<" Added " <<  added; 
      cout<< " Times, removed " << removed << " Times" << endl;
  j++;
  }

//------------------------------------------------------------------------------------------------------
  return 0;
};

