/* 
输入实例：

###### input for AIpine Club ######
# A(tony)
# A(mike)
# A(john)
# L(tony, rain)
# L(tony, snow)
# ~A(x), S(x), C(x)
# ~C(y), ~L(y, rain)
# L(z, snow), ~S(z)
# ~L(tony, u), ~L(mike, u)
# L(tony, v), L(mike, v)
# ~A(w), ~C(w), S(w)
###################################


#### input for hardworker(sue) ####
# GradStudent(sue)
# ~GradStudent(x), Student(x)
# ~Student(x), HardWorker(x)
# ~HardWorker(sue)
###################################

####### input for 3' blocks #######
# On(aa, bb)
# On(bb, cc)
# Green(aa)
# ~Green(cc)
# ~On(x, y), ~Green(x), Green(y)
###################################

*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

/*
    用于存储子句的容器。
    每一层 vector<string> 存储一个谓词语句，结构为：
        | 是否为真 | 函数名 | 量名 | 量名 | 。。。|
    其中是否为真用字符“0”表示假，字符“1”表示真。
    每一层 vector<vector<string>> 表示一个子句，因为一个子句中常有多个谓词语句。
        | 是否为真 | 函数名 | 量名 | 量名 | 。。。|
        | 是否为真 | 函数名 | 量名 | 量名 | 。。。|
        | 是否为真 | 函数名 | 量名 | 量名 | 。。。|
        。。。。。。
    最外层则是所有子句的集合。
*/
vector<vector<vector<string>>> clauses;
vector<string> results;
int nowClauses = 0; // 当前子句位置
int numClauses = 0; // 字句数量
int found = 0;     // 没找到
// int lastFound = 0;
bool checkout = 0;  // 无重复
int initNumClauses = 0;  // 初始子句数量

/* 
    用来判断是否为常量，因为题目友好，只要判断长度是否为1即可 
    常量返回1（长度大于1），变量返回0
*/
bool whether_const(string &s1){
    return !(s1.size() == 1);
}

void show(){
    cout << "--------------------------------------------------" << endl;
    for(int i = 0; i < clauses.size(); i ++){
        if(i < 10) cout << "  ";
        else if(i < 100) cout << " ";
        cout << i << "> ";
        for(int j = 0; j < clauses[i].size(); j ++){
            for(int k = 0; k < clauses[i][j].size(); k ++){
                cout << clauses[i][j][k] << " ";
            }
            cout << " | ";
        }
        cout << endl;
    }
    cout << "--------------------------------------------------"<< endl;
}

void removeUselessCons(){
    int toBeChanged[results.size()] = {0};
    for(int i = 0; i < initNumClauses; i ++) toBeChanged[i] = i + 1;
    int now_num = results.size() - 1;
    toBeChanged[now_num] = initNumClauses + 1;
    while(now_num >= initNumClauses){
        for(int j = 0; j < results[now_num].size(); j ++){
            if(results[now_num][j] >= '0' && results[now_num][j] <= '9'){
                int num_before_now = 0, a_pos = results[now_num][j] - '1';
                if(results[now_num][j + 1] >= '0' && results[now_num][j + 1] <= '9'){
                    a_pos = (a_pos + 1) * 10 + results[now_num][j + 1] - '1';
                    j ++;
                    if(results[now_num][j + 1] >= '0' && results[now_num][j + 1] <= '9'){
                        a_pos = (a_pos + 1) * 10 + results[now_num][j + 1] - '1';
                        j ++;
                    }
                }
                if(toBeChanged[a_pos] == 0){
                    for(int k = 0; k < a_pos; k ++){
                        if(toBeChanged[k] != 0) num_before_now ++;
                    }
                    toBeChanged[a_pos] = num_before_now + 1;
                    for(int k = a_pos + 1; k < results.size(); k ++){
                        if(toBeChanged[k] != 0) toBeChanged[k] ++;
                    }
                }
            }
        }
        now_num --;
        while(toBeChanged[now_num] == 0) now_num --;
    }
    // for(int i = 0; i < results.size(); i ++){
    //     if(toBeChanged[i] != 0) cout << i << " ";
    // }
    // cout << endl;
    int num_results = results.size(), num_removed = 0;
    for(int i = 0; i < num_results; i ++){
        // cout << results[i - num_removed] << " " << endl ;
        if(toBeChanged[i] == 0){
            results.erase(results.begin() + i - num_removed);
            num_removed ++;
        }
        else{
            // cout << i << " " << i - num_removed << endl;
            for(int j = 0; j < results[i - num_removed].size(); j ++){
                if(results[i - num_removed][j] >= '0' && results[i - num_removed][j] <='9'){
                    int a_pos = results[i - num_removed][j] - '1', moreThanTen = 0, moreThanHun = 0;
                    if(results[i - num_removed][j + 1] >= '0' && results[i - num_removed][j + 1] <= '9'){
                        a_pos = (a_pos + 1) * 10 + results[i - num_removed][j + 1] - '1';
                        j ++;
                        moreThanTen = 1;
                        if(results[i - num_removed][j + 1] >= '0' && results[i - num_removed][j + 1] <= '9'){
                            a_pos = (a_pos + 1) * 10 + results[i - num_removed][j + 1] - '1';
                            j ++;
                            moreThanHun = 1;
                        }
                    }
                    // cout << a_pos << " ";
                    if(moreThanHun && toBeChanged[a_pos] >= 100){
                        results[i - num_removed][j] = toBeChanged[a_pos] % 10 + '0';
                        results[i - num_removed][j - 1] = toBeChanged[a_pos] / 10 % 10 + '0';
                        results[i - num_removed][j - 2] = toBeChanged[a_pos] / 100 + '0';
                    }
                    else if(moreThanHun && toBeChanged[a_pos] >= 10){
                        results[i - num_removed][j - 1] = toBeChanged[a_pos] % 10 + '0';
                        results[i - num_removed][j - 2] = toBeChanged[a_pos] / 10 + '0';
                        results[i - num_removed].erase(results[i - num_removed].begin() + j);
                        j --;
                    }
                    else if(moreThanTen && toBeChanged[a_pos] >= 10){
                        results[i - num_removed][j] = toBeChanged[a_pos] % 10 + '0';
                        results[i - num_removed][j - 1] = toBeChanged[a_pos] / 10 + '0';
                    }
                    else if(moreThanTen && toBeChanged[a_pos] < 10){
                        results[i - num_removed][j - 1] = toBeChanged[a_pos] + '0';
                        results[i - num_removed].erase(results[i - num_removed].begin() + j);
                        j --;
                    }
                    else{
                        results[i - num_removed][j] = toBeChanged[a_pos] + '0';
                    }
                }
            }
            // cout << endl;
        }
    }
}

/* 
    每次都要检测当前子句集中是否有重复的项 
    有重复返回1
*/
bool check(vector<vector<string>> &ivvarr){
    for(int i = 0; i < clauses.size(); i ++){
        if(ivvarr == clauses[i]){
            checkout = 1;
            return 1;
        }
    }
    return 0;
}

/* 
    检测是否真的找到解 
    因为中途遇到直接用条件里的两个子句归结得到空的情况
    （说的就是你！AIpine_Club的
        ~L(tony, u), ~L(mike, u)
        L(tony, v), L(mike, v)
    就离谱！）
*/
// bool checkFound(int x1, int x2){
//     if(x1 > initNumClauses - 1 && x2 > initNumClauses - 1){
//         int x1a_pos = -1, x1b_pos = -1, x2a_pos = -1, x2b_pos = -1;
//         for(int j = 0; j < results[x1].size(); j ++){
//             if(results[x1][j] >= '0' && results[x1][j] <= '9'){
//                 int pos = results[x1][j] - '1';
//                 if(results[x1][j + 1] >= '0' && results[x1][j + 1] <= '9'){
//                     pos = (pos + 1) * 10 + results[x1][j + 1] - '1';
//                     j ++;
//                 }
//                 if(x1a_pos < 0) x1a_pos = pos;
//                 else x1b_pos = pos;
//             }
//         }
//         for(int j = 0; j < results[x2].size(); j ++){
//             if(results[x2][j] >= '0' && results[x2][j] <= '9'){
//                 int pos = results[x2][j] - '1';
//                 if(results[x2][j + 1] >= '0' && results[x2][j + 1] <= '9'){
//                     pos = (pos + 1) * 10 + results[x2][j + 1] - '1';
//                     j ++;
//                 }
//                 if(x2a_pos < 0) x2a_pos = pos;
//                 else x2b_pos = pos;
//             }
//         }
//         cout << x1a_pos << x1b_pos << x2a_pos << x2b_pos << endl;
//         if(x1a_pos >= 0) return checkFound(x1a_pos, x1b_pos) || checkFound(x2a_pos, x2b_pos);
//         else return false;
//     }
//     else if(x1 == initNumClauses - 1 || x2 == initNumClauses - 1) return true;
//     else if(x1 < initNumClauses - 1 && x2 < initNumClauses - 1) return false;
// }

/*
    每次检测字句内是否有可归结或重复的项
*/
vector<vector<string>> insideCheck(vector<vector<string>> &ivvarr){
    for(int i = 0; i < ivvarr.size(); i ++){
        for(int j = i + 1; j < ivvarr.size(); j ++){
            if(ivvarr[i][1] != ivvarr[j][1]){
                continue;
            }
            else{
                int f1 = 1;
                for(int k = 2; k < ivvarr[i].size(); k ++){
                    if(ivvarr[i][k] != ivvarr[j][k]){
                        f1 = 0;
                    }
                }
                if(f1){
                    if(ivvarr[i][0] != ivvarr[j][0]){
                        ivvarr.erase(ivvarr.begin() + j);
                        ivvarr.erase(ivvarr.begin() + i);
                    }
                    else{
                        ivvarr.erase(ivvarr.begin() + j);
                    }
                }
            }
            
        }
    }
    return ivvarr;
}

vector<pair<string, pair<int, string>>> MGU(int x1, int y1, int x2, int y2, int size){
    vector<pair<string, pair<int, string>>> toBeUpdate;
    vector<pair<string, pair<int, string>>> nonUpdate;
    for(int i = 2; i < size; i ++){
        // cout << clauses[x1][y1][i] << " " << clauses[x2][y2][i] << endl;
        if(!(whether_const(clauses[x1][y1][i]) && whether_const(clauses[x2][y2][i]))){
            if(!whether_const(clauses[x1][y1][i])){
                toBeUpdate.push_back(make_pair(clauses[x1][y1][i], make_pair(i, clauses[x2][y2][i])));
            }
            else{
                toBeUpdate.push_back(make_pair(clauses[x2][y2][i], make_pair(i, clauses[x1][y1][i])));
            }
        }
        else{
            if(clauses[x1][y1][i] == clauses[x2][y2][i]){
                toBeUpdate.push_back(make_pair(clauses[x1][y1][i], make_pair(i, clauses[x2][y2][i])));
            }
            else{
                 return nonUpdate;
            }
        }
    }
    vector<vector<string>> ivtem1(clauses[x1]), ivtem2(clauses[x2]);
    if(toBeUpdate.size()){
        ivtem1.erase(ivtem1.begin() + y1);
        ivtem2.erase(ivtem2.begin() + y2);
        for(int i = 0; i < toBeUpdate.size(); i ++){
            for(int v = 0; v < ivtem1.size(); v ++){
                for(int j = 2; j < size; j ++){
                    if(ivtem1[v][j] == toBeUpdate[i].first){
                        ivtem1[v][j] = toBeUpdate[i].second.second;
                    }
                }
            }
            for(int v = 0; v < ivtem2.size(); v ++){
                for(int j = 2; j < size; j ++){
                    if(ivtem2[v][j] == toBeUpdate[i].first){
                        ivtem2[v][j] = toBeUpdate[i].second.second;
                    }
                }
            }
        }
        vector<vector<string>> ivvtemp;
        ivvtemp.insert(ivvtemp.end(), ivtem1.begin(), ivtem1.end());
        ivvtemp.insert(ivvtemp.end(), ivtem2.begin(), ivtem2.end());
        vector<vector<string>> ivvttemp = insideCheck(ivvtemp);
        if(ivvttemp.size() == 0){
            vector<string> ivttempNull;
            ivttempNull.push_back(string("2"));
            vector<vector<string>> ivvttempNull;
            ivvttempNull.push_back(ivttempNull);
            clauses.push_back(ivvttempNull);
            numClauses ++;
            if(x1 >= initNumClauses && x2 >= initNumClauses) found = 1;
            // show();
            // if(checkFound(x1, x2)) found += 1;
            // else{
            //     // cout << "a" << endl;
            //     vector<string> ivttempNull;
            //     ivttempNull.push_back(string("2"));
            //     vector<vector<string>> ivvttempNull;
            //     ivvttempNull.push_back(ivttempNull);
            //     clauses.push_back(ivvttempNull);
            //     numClauses ++;
            //     //show();
            // }
        }
        else if(!check(ivvttemp)){
            clauses.push_back(ivvttemp);
            numClauses ++;
        }
        // show();
        // for(int j = 0; j < clauses.back().size(); j ++){
        //     cout << " | ";
        //     for(int k = 0; k < clauses.back()[j].size(); k ++){
        //         cout << clauses.back()[j][k] << " ";
        //     }
        // }
        // cout << endl;
    }
    return toBeUpdate;
}

void do_big_things(){
    if(clauses[nowClauses][0][0][0] == '2') return;
    int max = numClauses;
    for(int i = 0; i < clauses[nowClauses].size(); i ++){
        char needTruth = '1' + '0' - clauses[nowClauses][i][0][0];
        string needFuncName = clauses[nowClauses][i][1];
        // cout << needTruth << " " << needFuncName << endl;
        for(int j = 0; j < max; j ++){
            if(j == nowClauses) continue;
            for(int k = 0; k < clauses[j].size(); k ++){
                if(found == 1) break;
                if(clauses[j][k][0][0] == needTruth && clauses[j][k][1] == needFuncName){
                    // cout << nowClauses << " " << i << " " << j << " " << k << " " << endl;
                    vector<pair<string, pair<int, string>>> updated = MGU(nowClauses, i, j, k, clauses[j][k].size());
                    // if(found == 1) cout << "b" << endl;
                    if(updated.size()){
                        string sstemp = "R[";
                        sstemp += to_string(nowClauses + 1);
                        if(clauses[nowClauses].size() > 1){
                            sstemp += string("a");
                            sstemp[sstemp.size() - 1] += i;
                        }
                        sstemp += string(", ");
                        sstemp += to_string(j + 1);
                        if(clauses[j].size() > 1){
                            sstemp += string("a");
                            sstemp[sstemp.size() - 1] += k;
                        }
                        sstemp += string("] {");
                        for(int v = 0; v < updated.size(); v ++){
                            if(!(updated[v].first == updated[v].second.second && (whether_const(updated[v].first) && whether_const(updated[v].second.second)))){
                                sstemp += updated[v].first;
                                sstemp += string("=");
                                sstemp += updated[v].second.second;
                                if(v != updated.size() - 1) sstemp += string(",");
                            }
                            // else{
                            //     sstemp += string(" ");
                            // }
                        }
                        if(sstemp.back() == ',') sstemp.erase(sstemp.end() - 1);
                        sstemp += string("} : ");
                        // if(clauses.back().size() > 1){
                        //     sstemp += string("(");
                        // }
                        if(!found){
                            // cout << "b" << endl;
                            for(int v = 0; v < clauses.back().size(); v ++){
                                // cout << "c" <<endl;
                                if(clauses.back()[v][0] == "0"){
                                    sstemp += string("~");
                                }
                                else if(clauses.back()[v][0] == "2"){
                                    sstemp += string("( )");
                                    break;
                                }
                                sstemp += clauses.back()[v][1];
                                sstemp += string("(");
                                for(int n = 2; n < clauses.back()[v].size(); n ++){
                                    sstemp += clauses.back()[v][n];
                                    if(n != clauses.back()[v].size() - 1) sstemp += string(", ");
                                }
                                sstemp += string(")");
                                if(v != clauses.back().size() - 1) sstemp += string(",");
                            }
                            
                        }
                        else{
                            sstemp += string("( )");
                            // lastFound = found;
                        }
                        if(!checkout){
                            results.push_back(sstemp);
                        }
                        else{
                            checkout = 0;
                        }
                        // cout << "end in : " << results.size() << endl;
                    }
                }
            }
        }
    }
}

int main(){
    string filename = "hardworker.txt";        // 测例文件，修改文件名即可测试不同测例
    ifstream pfile;
    string buf;
    pfile.open(filename.c_str());

    /* 
        以下是将输入转化为clauses指定格式的过程
        注意，题目友好（指一个谓词语句只有一对）时才成立 
    */
    while(getline(pfile, buf)){
        numClauses ++;
        results.push_back(buf);
        vector<string> iv;
        vector<vector<string>> ivv;
        int newOne = 1;
        for(int i = 0; i < buf.size(); i ++){
            if(newOne == 1){
                if(buf[i] == '~'){
                    iv.push_back(string(1, '0'));
                    newOne = 0;
                    continue;
                }
                else{
                    iv.push_back(string(1, '1'));
                    newOne = 0;
                    int j = i;
                    string funcName, vcName;
                    while(buf[j] != '('){       // 读取函数名
                        funcName += buf[j];
                        j ++;
                    }
                    iv.push_back(funcName);
                    j ++;
                    while(buf[j] != ')'){       // 读取量名，变量常量都读进来
                        if(buf[j] == ','){
                            iv.push_back(vcName);
                            vcName.clear();
                            j += 2;
                        }
                        else{
                            vcName += buf[j];
                            j ++;
                        }
                    }
                    iv.push_back(vcName);
                    i = j + 2;
                    newOne = 1;
                    ivv.push_back(iv);
                    iv.clear();
                }
            }
            else{
                int j = i;
                string funcName, vcName;
                while(buf[j] != '('){       // 读取函数名
                    funcName += buf[j];
                    j ++;
                }
                iv.push_back(funcName);
                j ++;
                while(buf[j] != ')'){       // 读取量名，变量常量都读进来
                    if(buf[j] == ','){
                        iv.push_back(vcName);
                        vcName.clear();
                        j += 2;
                    }
                    else{
                        vcName += buf[j];
                        j ++;
                    }
                }
                iv.push_back(vcName);
                i = j + 2;
                newOne = 1;
                ivv.push_back(iv);
                iv.clear();
            }
        }
        // for(int i = 0; i < ivv.size(); i ++){
        //     for(int j = 0; j < ivv[i].size(); j ++){
        //         cout << ivv[i][j] << " ";
        //     }
        //     cout << endl;
        // }
        clauses.push_back(ivv);
    }
    initNumClauses = numClauses;
    //show();
    while(nowClauses < clauses.size()){
        do_big_things();
        nowClauses ++;
        if(found == 1) break;
    }

    /* test */
    // nowClauses = 3;
    // do_big_things();

    //cout << results.size() << endl;
    // for(int i = 0; i < results.size(); i ++){
    //     if(i + 1 < 10) cout << "  ";
    //     else if(i + 1 < 100) cout << " ";
    //     cout << i + 1 << "> " << results[i] << endl;
    // }
    // show();
    removeUselessCons();
    for(int i = 0; i < results.size(); i ++){
        if(i + 1 < 10) cout << "  ";
        else if(i + 1 < 100) cout << " ";
        cout << i + 1 << "> " << results[i] << endl;
    }
}
