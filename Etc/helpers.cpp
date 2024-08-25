#include "helpers.hpp"

vector<string> tokenizer(string s, char del)
{
    vector<string> result;
    stringstream ss(s);
    string word;
    while (!ss.eof()) {
        getline(ss, word, del);
        result.push_back(word);
    }
    return result;
}
