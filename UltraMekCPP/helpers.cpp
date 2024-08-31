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

string remove_closure(string token)
{
    token.pop_back();
    token.erase(token.begin());   
    return token;
}

void ltrim_inplace(string &s) 
{
    s.erase(s.begin(), find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !isspace(ch);
    }));
}

void rtrim_inplace(string &s)
{
    s.erase(find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !isspace(ch);
    }).base(), s.end());
}

void trim_inplace(string &s) {
    rtrim_inplace(s);
    ltrim_inplace(s);
}

string ltrim(string s) 
{
    ltrim_inplace(s);
    return s;
}

string rtrim(string s) 
{
    rtrim_inplace(s);
    return s;
}

string trim(string s) 
{
    trim_inplace(s);
    return s;
}
