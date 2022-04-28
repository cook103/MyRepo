//Marcus Cook // cook103@cougars.csusm.edu // 004893042
#include <iostream>
using namespace std;


struct edge{
   int adj_vtx;  // index of adjacent vertex
   edge *next;   // the link to the next node in the list.
};

class BFSQueue{
private:
	 int* Arr;
 	 int Front = 0;
	 int Rear = -1;
	 int SIZE; 
    
public:
   int IsEmpty();
   void Enqueue(int);
   int Dequeue();
   int gFront(); //get the front of queue

   BFSQueue(int Vertex){   //constructor

   SIZE = (2 * Vertex);
   Arr = new int[SIZE];
	 int i = 0;
    
   while(i < SIZE){
		Arr[i] = -1;
		i++;
    }
	}

};

class Graph{
private:
  int V;         // No. of vertices 
  edge **adj;   // Pointer to an array containing adjacency lists 
  int count;
  
  int *visited;  //variables in BFS func.
  int *p1;
  int *p2; 


  void DFSUtil(int v, bool visited[]){  // A function used by DFS 
  edge * key;  
  visited[v] = true;

  key = adj[v];
  cout << " " << v ;
  
  while(key!=NULL){
  while(visited[key->adj_vtx] != true){	
    	DFSUtil(key->adj_vtx, visited);
	}
		
    key = key->next;
  }
}

public:        
     void addEdge(int v, int w); // function to add an edge to graph 
     void NumberOfEdges();
     void PrintGraph();
     void BFS(int);            // BFS traversal of the vertices reachable from s
     void DFS(int);            // DFS traversal of the vertices reachable from v 
     bool hasCycle();             // Check whether the graph has cycles
     void Traverse(int, int[]);
     void DriverProgram();
    

  Graph(int V){   // Constructor 
  if(V >= 0){
    adj = new edge*[V]; //creating new edge
    this->V = V;
  } 
    int i = 0;
    while(i < V){
      adj[i] = NULL;
     
     i++;
   }
 }

};

//Basic Queue Class Functions

int BFSQueue::IsEmpty(){
	if(Front > Rear){
		return 1;
	}
	  return 0;
}

void BFSQueue::Enqueue(int Value){
	Rear = Rear+1;
  Arr[Rear] = Value;
}
	
int BFSQueue::Dequeue(){
int F = -1;
SIZE = Front-1;
  
  if(Rear >= Front){
		Front = Front+1;
    return Arr[SIZE];
  }
  else
    return F;
}

	
int BFSQueue::gFront(){
	return Arr[Front];
}
	


//Graph Class Functions

void Graph::addEdge(int v, int w){
edge *key;
key = adj[v];

while(adj[v] == NULL){   //if list is empty
  adj[v] = new edge;     //create new Node/Edge
  adj[v]->adj_vtx = w;
  adj[v]->next = NULL;
  return;
  }
  if(v < 0){
    return;
  }
  if(v >= V){
    return;
  } 
while(key->next != NULL){ //while the list is not empty
      key = key->next;
    }
      key->next = new edge;
      key->next->adj_vtx = w;
      key->next->next = NULL;
      return;
}

   
void Graph::PrintGraph(){
 edge* key;
 int i = 0; 
 while(i < V){
	 key = adj[i];
   count = i;
 while(key!=NULL){
	 cout << key->adj_vtx;
  if(key->next){
    printf("-->");
   }
	 key = key->next;
	 }
	 cout << endl;
	i++;
  }
}

void Graph::BFS(int s){
  int head;
  BFSQueue start(V); //intializer (start)
  start.Enqueue(s);

  visited = new int; 
  visited[s] = 1;
 
  p1 = new int;
  p1[s] = -1;
                
  while(start.IsEmpty()!=1){
  
  head  = start.gFront(); 
  cout << " " << head;
  
  start.Dequeue();
  
  edge *key; 
  key = adj[head];
  
  while(key!=NULL){
  int temp = key->adj_vtx;
  if (!visited[temp]){
  visited[temp] = true;
  
  start.Enqueue(temp);
  p2 = new int;
  p2[temp] = (p2[head] + 1);
  p1[temp] = head;
  }
  
  key = key->next;
  }
  
  }

}
        
void Graph::DFS(int v){
  bool* visited;
  int i = 0;
  

  visited = new bool;
	
  while(i < V){
		 visited[i] = false;
     i++;	
  }
	DFSUtil(v, visited); cout << endl;

  cout << hasCycle() << endl;
}

void Graph::Traverse(int first, int T[]){
  edge* key;
		
   if(T[first] == true){
    printf("cycle Found");  //cycle found
    }
		key = adj[first];
    cout << "\nTraversing at --> " << first << "\n";    
   while(key!=NULL){
	  Traverse(key->adj_vtx, T);
		return;
    }
	 key = key->next;
	}

   
bool Graph::hasCycle(){
    int i,j;
    i = 0; 
    int* traverse = new int;	//check cycle call nodes
		while (i < V){
		
    for (j = 0; j < V; j++)
			{
				traverse[j] = -1;
			}
			int first = i;

//not finished
i++;  
 }
cout << "\n" ;
return true;

}

void Graph::DriverProgram(){
Graph graph(5); //create the graph (5 verticies)  

cout << "graph connections" << endl;
graph.addEdge(0, 1); //adding edges
graph.addEdge(0, 2);
graph.addEdge(0, 4);
graph.addEdge(1, 2);
graph.addEdge(1, 3);
graph.addEdge(2, 0);
graph.addEdge(2, 3);
graph.addEdge(3, 3);
graph.addEdge(3, 1);
graph.PrintGraph();
graph.NumberOfEdges();

cout << "BFS at vertex 2: \n";
graph.BFS(2); cout << "\n";
cout << "DFS at vertex 2: \n";
graph.DFS(2);

printf("\nTest A Vertex Here (BFS&DFS): ");
int startv; //starting vertex
cin>>startv; cout << "\n";

cout << "Breadth First Traversal Starting From Vertex " << startv <<  " = \n" << endl;
graph.BFS(startv); cout << endl;
cout << "Depth First Traversal Starting From Vertex " << startv <<  " = \n" << endl;
graph.DFS(startv);
}     

void Graph::NumberOfEdges(){
cout << "\n" ;
printf("Total Number of Edges = "); 
cout << count << "\n" << endl;
}
      

 


int main(){
Graph start(5);
start.DriverProgram();




return 0;
}