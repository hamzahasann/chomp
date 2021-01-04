#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

const int h=10,w=10;
int total_state=0;
vector<vector<ll>> rndb(h,vector<ll>(w));
map<ll,vector<int>>best_move;
map<ll,int>pos;

int cell_count(vector<vector<int>>grid);
ll zobrist(vector<vector<int>>grid);
vector<vector<int>>eat(vector<vector<int>>grid,int i,int j);
void assign_random();
void display(vector<vector<int>>);
void find_move(vector<vector<int>>);
void precompute_moves();
void test();
void write_randomboard();
void write_bestmoves();

int cell_count(vector<vector<int>>a){
	int c=0;
	for(int i=0;i<h;i++){
		for(int j=0;j<w;j++){
			c+=(a[i][j]==1);
		}
	}return c;
}
ll zobrist(vector<vector<int>>grid){
	ll hash=0;
	for(int i=0;i<grid.size();i++){
		for(int j=0;j<grid[0].size();j++){
			if(grid[i][j]){
				hash^=rndb[i][j];
			}
		}
	}return hash;
}
vector<vector<int>> eat(vector<vector<int>>a,int i,int j){
	for(int y=0;y<h;y++){
		for(int x=0;x<w;x++){
			if(y>=i && x>=j){
				a[y][x]=0;
			}
		}
	}return a;
}
void assign_random(){
	random_device rd;
	default_random_engine dre(rd());
	uniform_int_distribution<unsigned long long> dist(0,LLONG_MAX);
	for(int i=0;i<h;i++){
		for(int j=0;j<w;j++){
			rndb[i][j]=dist(dre);
		}
	}
}
void display(vector<vector<int>>a){
	for(int i=0;i<a.size();i++){
		for(int j=0;j<a[0].size();j++){
			cout<<a[i][j]<<" ";
		}cout<<endl;
	}
}
void find_move(vector<vector<int>>grid){
	ll hash=zobrist(grid);
	if(pos.find(hash)!=pos.end())return;
	total_state++;
	if(total_state%5000==0)cout<<total_state<<" states processed"<<endl;
	// display(grid);cout<<endl;
	for(int i=0;i<h;i++){
		for(int j=0;j<w;j++){
			if(grid[i][j]==1){
				vector<vector<int>>nxt=eat(grid,i,j);
				find_move(nxt);
				ll nxhash=zobrist(nxt);
				//find any losing state -> win
				//else lose
				if(pos[nxhash]==0){
					best_move[hash]={i,j};
					pos[hash]=1;
					// return;//pruning
				}
			}
		}
	}if(pos[hash]==0){
		best_move[hash]={0,0};
	}
	return;
}
void precompute_moves(){
	vector<vector<int>>dflt(h,vector<int>(w));
	//base case: empty grid -> win
	ll hash=zobrist(dflt);
	best_move[hash]={0,0};
	pos[hash]=1;
	total_state++;
	for(int i=0;i<h;i++){
		for(int j=0;j<w;j++){
			dflt[i][j]=1;
		}
	}find_move(dflt);
}
void test(){
	//debug
	int t;cin>>t;
	for(int tt=0;tt<t;tt++){
		vector<vector<int>>a(h,vector<int>(w));
		for(int i=0;i<h;i++){
			for(int j=0;j<w;j++){
				cin>>a[i][j];
			}
		}ll hash=zobrist(a);
		// cout<<pos[hash]<<endl;
		cout<<best_move[hash][0]<<" "<<best_move[hash][1]<<endl;
	}
}
void write_randomboard(){
	ofstream file;
	file.open("randomboard.txt");
	for(int i=0;i<h;i++){
		for(int j=0;j<w;j++){
			file<<rndb[i][j]<<endl;
		}
	}file.close();
}
void write_bestmoves(){
	ofstream file;
	file.open("bestmoves.txt");
	for(auto it:best_move){
		file<<it.first<<" "<<it.second[0]<<" "<<it.second[1]<<endl;
	}file.close();
}
int main(){
	// assign_random();
	// precompute_moves();
	// test();
	// write_randomboard();
	// write_bestmoves();
	// cout<<total_state<<endl;
}


/*


*/
