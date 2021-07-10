#include<iostream> 
#include<bits/stdc++.h>
using namespace std;

char Mazedata[100][100];                     //matrix of maze 
int sx, sy, ex, ey;                         //coordinate of start point and end point 
int shortdis=1000000;                      //the distance of the shortest path,start with 1000000 
bool visited[100][100];                   //have visited or not 
vector< pair<int, int> > dir;            //directions£ºW/A/S/D
vector< pair<int, int> > shortpath;     //record the shortest path

void dfs(int x,int y,int length,vector< pair<int, int> > &path){
visited[x][y]=1;
path.push_back(make_pair(x, y));
//update the shortest path when get to the end point 
if(x==ex&&y==ey){
if(length<shortdis){
shortdis=length;
shortpath=path;
}
return;
}
//search in all directions 
for(int i=0; i<dir.size(); i++){
int nx=x+dir[i].first;
int ny=y+dir[i].second;
if(Mazedata[nx][ny]!='1'&&visited[nx][ny]!=1){
length++;
dfs(nx,ny,length,path);
length--;
visited[nx][ny] = 0;
path.pop_back();
}  
}
return;
}

int main(){
int m=1, n;
//express the directions:W/A/S/D 
dir.push_back(make_pair(-1, 0));
dir.push_back(make_pair(0, -1));
dir.push_back(make_pair(0, 1));
dir.push_back(make_pair(1, 0));
//read the data of maze
ifstream input("MazeData.txt");
char s[100];
input.getline(s,100);
n=strlen(s);
strcpy(Mazedata[0],s);
while(!input.eof()){
visited[m][0]=1;
visited[m][n-1]=1;
for(int j=0;j<n;j++){
input>>Mazedata[m][j];
if(Mazedata[m][j]=='S'){
sx=m;
sy=j;
}
if(Mazedata[m][j]=='E'){
ex=m;
ey=j;
}		
}
m++;
}
m--;
input.close();
vector< pair<int, int> > path;
dfs(sx,sy,0,path);              //DFS
if(shortdis==1000000) cout<<"There is no solution to this question.\n";
else{
cout<<"the distance of the shortest path is£º"<<shortdis<<endl;
cout<<"the path is as follows:\n";
for(int i=1;i<shortpath.size()-1;i++) Mazedata[shortpath[i].first][shortpath[i].second]='#';
for(int i=0;i<m;i++){
for(int j=0;j<n;j++){
cout<<Mazedata[i][j];		
}
cout<<endl;
}
}
return 0;
}
