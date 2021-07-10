#include<iostream>
#include<stdio.h>
#include<cmath>
#include<string>
#include<cassert>
using namespace std;

#define N1 4
#define N2 16
#define LIMIT 100

static const int dx[4] = {0, -1, 0, 1};
static const int dy[4] = {1, 0, -1, 0};
static const char dir[4] = {'R', 'U', 'L', 'D'};
int MHD[N2][N2];

struct Puzzle{
	int f[N2],space,h; 
};

Puzzle state;
int limit;//Depth-limit
int path[LIMIT];

int geth(Puzzle puzzle){
	int sum=0;
	for(int i=0;i<N2;i++) {
		if(puzzle.f[i]==N2) continue;
		sum+=MHD[i][puzzle.f[i]-1];
	}
	return sum;
} 

bool solved(){
	for(int i=0;i<N2;i++) if(state.f[i]!=i+1) return false;
	return true;
}

bool dfs(int depth,int prev){
	if(state.h==0) return true;
	//If the current depth plus heuristic exceeds the limit, pruning.
	if(depth+state.h>limit) return false;
	int sx=state.space/N1;
	int sy=state.space%N1;
	Puzzle temp;
	for(int r=0;r<4;r++) {
		int tx=sx+dx[r];
		int ty=sy+dy[r];
		if(tx<0||ty<0||tx>=N1||ty>=N1)continue;
		if(max(prev,r)-min(prev,r)==2)continue;
		temp=state;
		//Calculate the difference of Manhattan distance and exchange the puzzle pieces
		state.h-=MHD[tx*N1+ty][state.f[tx*N1+ty]-1];
		state.h+=MHD[sx*N1+sy][state.f[tx*N1+ty]-1];
		swap(state.f[tx*N1+ty],state.f[sx*N1+sy]);
		state.space=tx*N1+ty;
		if(dfs(depth+1,r)){
			path[depth]=r; 
			return true; 
		}
		state=temp;
	} 
	return false;
}

//Iterative deepening
string ID(Puzzle puzzle) {
	puzzle.h=geth(puzzle);//Manhattan distance of initial state
	for(limit=puzzle.h;limit<=LIMIT;limit++) {
		state=puzzle;
		if(dfs(0,-100)){
			string ans="";
			for(int i=0;i<limit;i++) ans+=dir[path[i]];
			return ans;
		}
	} 
	
	return "No solution!";
} 

int main(){
	for(int i=0;i<N2;i++)
		for(int j=0;j<N2;j++)
			MHD[i][j]=abs(i/N1-j/N1)+abs(i%N1-j%N1);
	Puzzle fifpuzzle;
	for(int i=0;i<N2;i++){
		cin>>fifpuzzle.f[i];
		if(fifpuzzle.f[i]==0){
			fifpuzzle.f[i]=N2;
			fifpuzzle.space=i;
		}
	}
	string ans=ID(fifpuzzle);
	cout<<ans.size()<<endl;
	return 0;
}

