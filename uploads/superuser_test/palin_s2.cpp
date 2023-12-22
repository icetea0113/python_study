#include <iostream>
#include <cmath>

using namespace std;

string palin;

bool is_quasi(int start, int last){
    while(start<=last){
        if(palin[start]==palin[last]){
            start++;
            last--;
        }
        else return false;
    }
    return true;
} //end of is_quasi

int is_palin(){
    int start = 0, last = palin.size()-1;
    while(start<=last){
        if(palin[start]==palin[last]){
            start++;
            last--;
        }
        else{
            if(is_quasi(start+1, last)) return 2;
            else if(is_quasi(start, last-1)) return 2;
            else return 3;
        }
    }
    return 1;
} //end of is_palin

int main() {
    int N, res;
    cin >> N;

    while(N--) {
        cin >> palin;
        cout << is_palin() << "\n";
    }

    return 0;
} //end of main()