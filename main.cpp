//Marcus Cook // cook103@cougars.csusm.edu // 004893042
#include <iostream>
#include <string>
using namespace std;


class MaxHeap
{      
    private:
        int *arr;
        int capacity,max;
        int size,len,count;
   
    public:
       MaxHeap(int capacity);   
          
       int parent(int i){
       return (i-1)/2; 
       }      

       int left(int i){ 
       return (2*i + 1);
       }

       int right(int i){ 
       return (2*i + 2); 
      }

 
       void printArray(int arr[],int);  
       void setheapify(int A[],int,int);
       void heapify(int A[],int);
       void swap(int *, int *);
       void heapsort(int A[], int);
       void siftup(int);
       void siftdown(int);
       void insert(int);
       int removeAt(int);
       bool isLeaf(int);
       void switchcase();
       int extractMax();
 
};      

MaxHeap::MaxHeap(int cap){  //constructor
    size = 0; 
    capacity = cap; 
    arr = new int[cap];
    
}



bool MaxHeap::isLeaf(int i){
  if(i < size/2){
    return true;
  }
  else{
    return false;
 }
}

void MaxHeap::siftup(int i){
    while(i > 0 && arr[parent(i)] > arr[i]){
        swap((&arr[i]), (&arr[parent(i)]));
        i = parent(i);
    }
}

void MaxHeap::siftdown(int i){
  while(!isLeaf(i)){
    int L = left(i);
    int R = right(i);
    int smaller = L;
  if(R < size)
    smaller = (arr[L] < arr[R]);  
    if(arr[i] <= arr[smaller])
    break;
    swap(&arr[i], &arr[smaller]);
     i = smaller;

  }
}

void MaxHeap::printArray(int arr[], int len){  
 int i = 0;
 while(i < len){
    cout << arr[i] << " " ;
    i++;
    }
cout << "\n \n";  
}  

void MaxHeap::swap(int *a, int *b){  
int temp = *a;  
   *a = *b;  
   *b = temp;  
}  

void MaxHeap::insert(int k){
if (size > capacity)
cout << "\nOverflow: Could not insertKey\n";
int i = size;
arr[i] = k;
//cout << " " << k ;
siftup(i);
size++;
}


void MaxHeap::setheapify(int arr[], int len, int root_i){  

int L = left(root_i);
int R = right(root_i);
int max = root_i;  //setting max index 

while(arr[L] > arr[max] && L<len){ 
    max = L;      //if arr L is > take left index 
if (arr[R] > arr[max] && R<len) 
    max = R;     //if array R is greater take right index
if(root_i != max)
    { 
     swap(&arr[root_i], &arr[max]);
     setheapify(arr, len, max); //recursive
    } 
 }
}

void MaxHeap::heapify(int arr[], int len){  
  setheapify(arr,len,max); 
  printArray(arr,len);
}


void MaxHeap::heapsort(int arr[], int len){
int i = (len/2)-1;
  
  while(i >= 0){
  setheapify(arr,len,i); i--;  //build heap
  }
  for (i = len-1; i >= 0; i--){//extracting elements from heap
    swap(&arr[0],&arr[i]);
    setheapify(arr,i,0); //turn into heap
    } 
  printArray(arr,len);
}

int MaxHeap::removeAt(int i){
if(size == 1){ 
   return arr[--size];
}
    int result = arr[i]; 
    arr[i] = arr[--size];

if(arr[i] > result){ 
   siftdown(i);
}
else{ 
   siftup(i); }
   return result;
}

int MaxHeap::extractMax(){                   //NOT SURE ON THIS ONE
if(size < 0) 
cout << "overflow" << endl;
if(size == 1) 
return arr[--size];

int result = arr[0];
arr[0] = arr[--size];
siftup(-1);
return result;
}


void MaxHeap::switchcase(){
size = len;

cout << "(Refrence test case) 4,10,3,5,1, \n" << endl; 

cout << "how mant elements would you like to place in heap?" << endl; 
cin >> len; cout << "\n";
capacity = len;
int r = len-1;
MaxHeap maxheap(capacity); // creating the size of the heap
cout << "enter your elements" << endl;
for (int i=0; i <= r; i++){
cin >> arr[i];
maxheap.insert(arr[i]); //inserting input values
count++;
}
int c;
cout<< "\n1.Show Array \n" <<"2.Heapify\n" << "3.Heap Sort \n" << "4.Extract Max\n" << "5.Remove\n" << "6.Insert\n"<< endl; 
cin >> c;
cout << "\n";
cout << "You entered" << " " << c << "." <<endl;

switch(c){
case 1:{
cout << "Your Array = ";
maxheap.printArray(arr,len);
break;  
}
case 2:{
cout << "Heapify --> Forming Heap = ";
maxheap.heapify(arr,len);
break;
}
case 3:{
cout << "Heap Sort --> = ";
maxheap.heapsort(arr,len);
break;
}
case 4:{
cout << "extracting max --> = ";
cout << "max --> " << maxheap.extractMax()<< endl;
break;
}
case 5:{
cout << "what index would you like to remove from?" << endl;
int key; cin >> key;
if(key <= len){
cout << "removing index " << "--> " << key;
cout << " (which = " << removeAt(key) << ")" << endl;
cout << "heap is now --> ";
maxheap.heapify(arr,len);
}

else{
cout << "index does not exist!" << endl;
cout << "try again" << endl;
}

}
case 6:{
cout << "Enter a number to be inserted" << endl;
int key; cin >>key;
cout << "inserting key into max heap " << "--> ";
len++;
arr[len-1] = key;
maxheap.insert(key);
maxheap.heapify(arr,len);


}

}

}

//cout << "\nshould = 10 5 3 4 1" << endl;




int main() {
MaxHeap maxheap(100);
maxheap.switchcase();




return 0;
}