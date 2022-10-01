#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>
#include <unistd.h>

using namespace std;

string exec_error = "";

vector <string> split(string text, char stop){
    vector <string> result; string current;
    for(int i=0; i < text.length(); i++){
        if(text.at(i) == stop){
            result.push_back(current);
            current = "";
        }else{current += text.at(i);}
    }
    if(current != ""){result.push_back(current);}
    return result;
}

void call_error(string text, int line, int column, string description){
    if(exec_error == ""){
        vector <string> lines = split(text, '\n');
        string padding = "";
        for(int i = 0; i < column; i++){padding += " ";}
        exec_error = "Error at line " + to_string(line) + " column " + to_string(column) + ".\n";
        exec_error += "  " + lines[line] + "\n";
        exec_error += "  " + padding + "^\n";
        exec_error += description;
    }
}

void print_memory(vector <int> memory, int head){
    string actual = "", padding = "";
    for(int i=0; i < memory.size(); i++){
        actual += to_string(memory[i]);
        actual += ", ";
    }
    for(int i=0; i < 3 * head; i++){padding += " ";}
    actual += "\n" + padding + "^\n";
    actual += padding + to_string(head) + "\n";
    cout << actual << endl;
}

vector < vector <int> > find_loops(string text){
    vector <int> starts, ends;
    vector < vector <int> > loops;
    string error = ""; int line = 0, column = -1;
    for(int i = 0; i < text.length(); i++){
        char letter = text[i];
        if(letter == '\n'){line += 1; column = 0;}
        else{
            if(letter == '['){starts.push_back(i);}
            else if(letter == ']'){ends.push_back(i);}
            column += 1;
        }
    }
    if(starts.size() != ends.size()){
        call_error(text, line, column, "Unmatching brackets.");
    }

    int length = starts.size();
    for(int i = 0; i < length; i++){
        int start = starts[length-i-1], end = -1, record = text.length(), best_index = 0;
        for(int j = 0; j < ends.size(); j++){
            if(ends[j] - start < record && ends[j] - start > 0){
                best_index = j;
                record = ends[j] - start;
            }
        }
        end = ends[best_index];
        ends.erase(ends.begin() + best_index);
        vector <int> loop {start, end};
        loops.push_back(loop);
    }

    return loops;
}

string run(string text, bool debug){
    vector <int> memory{0};
    vector < vector <int> > loops = find_loops(text);
    int head = 0; string result = "";
    int index = 0, line = 0, column = 0;

    // cout << text << endl;
    while(index < text.length()){
        if(exec_error.length() != 0){ return exec_error;}
        char current = text.at(index);
        if(current == '\n'){
            line += 1; column = 0; index += 1;
        }else{
            if(current == ' ' || current == '\t' || current == '['){}
            else if(current == '='){ print_memory(memory, head); }
            else if (current == '>'){
                head += 1;
                if(head == memory.size()){ memory.push_back(0); }
            }
            else if (current == '<'){
                head -= 1;
                if(head < 0){ call_error(text, line, column, "Memory out of bounce"); }
            }
            else if(current == '+'){ memory[head] += 1; }
            else if(current == '-'){
                if(memory[head] > 0){ memory[head] -= 1; }
                else{
                    call_error(
                        text, line, column,
                        "Invalid negative counter at "
                        + to_string(head) + " memory."
                    );
                }
            }
            else if(current == '.'){ result += char(memory[head]); }
            else if(current == ']'){
                for(int i = 0; i < loops.size(); i++){
                    int start = loops[i][0], end = loops[i][1];
                    if(end == index && memory[head] != 0){ index = start; }
                }
            }
        }
        index += 1; column += 1;
        if(debug == true){
            print_memory(memory, head);
            // system("cls");
            sleep(0.5);
        }
    }
    return result;
}

int main(){

    string code;
    cin >> code;
    vector < vector <int> > loops = find_loops(code);
    // for(int i = 0; i < loops.size(); i++){
    //     cout << loops[i][0] << loops[i][1] << endl;
    // }
    string result = run(code, false);
    if(result != ""){
        cout << result << endl;
    }

    return 0;
}