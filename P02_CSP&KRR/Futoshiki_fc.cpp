#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <ctime>
#include <chrono>
using namespace std;
using namespace std::chrono;

long num_of_nodes = 0;                      // 用来计算拓展的节点数
double sum_time = 0.0;                      // 上述的和

class Futoshiki {
public:
    int size;
    int con_num;
    vector<vector<int>> puzzle;
    vector<pair<pair<int, int>, pair<int, int>>> constraints;

    Futoshiki(const char* puz_filename, const char* con_filename, int size, int con_num);                 
    bool isSolved();
    vector<vector<set<int>>> makeDomains();
    vector<vector<set<int>>> updateDomains(vector<vector<set<int>>> domains, const pair<int, int>& pos); 
    pair<int, int> mrv(const vector<vector<set<int>>>& domains);
    vector<vector<int>> forwardChecking(const vector<vector<set<int>>>& domains);

private:
    // 可取值的个数
    int domainCount(const vector<vector<set<int>>>& domains) {
        int count = 0;
        for(int i = 0; i < size; i++) {
            for(int j = 0; j < size; j++) {
                count += domains[i][j].size();
            }
        }
        return count;
    }
};

/*
    从文件“puzzlex.txt”和“constraintsx.txt”中分别读取初始谜题和限制。
    限制中的坐标是从（0,0）开始的。
*/
Futoshiki::Futoshiki(const char* puz_filename, const char* con_filename, int size, int con_num)
    : size(size), con_num(con_num), puzzle(size, vector<int>(size, 0)) {
    ifstream puz_file(puz_filename), con_file(con_filename);
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            puz_file >> puzzle[i][j];
        }
    }

    for (int i = 0; i < con_num; i++) {
        int x1, y1, x2, y2;
        con_file >> x1 >> y1 >> x2 >> y2;
        // 这里不要 x-1, y-1什么的 ！！！！从0开始。
        constraints.push_back(make_pair(make_pair(x1, y1), make_pair(x2, y2)));
    }
    puz_file.close();
    con_file.close();
}

/* 如果所有空都被填上则解题完成 */
bool Futoshiki::isSolved() {
    for (int i = 0; i < puzzle.size(); i++) {
        for (int j = 0; j < puzzle[0].size(); j++) {
            if (puzzle[i][j] == 0) {
                return false;
            }
        }
    }
    return true;
}

vector<vector<set<int>>> Futoshiki::makeDomains() {
    // 初始化x*x*9的三维矩阵
    vector<vector<set<int>>> domains(size, vector<set<int>>(size, set<int>()));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] == 0) {
                for (int k = 1; k <= size; k ++) {
                    domains[i][j].insert(k);
                }
            } else {
                domains[i][j].insert(puzzle[i][j]);
            }
        }
    }

    // 根据行列限制删除部分取值（同行同列数字不重复）
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] != 0) {
                for (int i2 = 0; i2 < size; i2++) {
                    if (i2 != i) {
                        domains[i2][j].erase(puzzle[i][j]);
                    }
                }
                for (int j2 = 0; j2 < size; j2++) {
                    if (j2 != j) {
                        domains[i][j2].erase(puzzle[i][j]);
                    }
                }
            }
        }
    }

    // 根据小于限制删除部分取值
    int old_domain_count = 0, new_domain_count;
    // 外层while循环使得这个循环执行到任何值域都不能缩小为止
    do {
        for (int i = 0; i < con_num; i++) {
            pair<int, int> small_pos = constraints[i].first;
            pair<int, int> large_pos = constraints[i].second;
            if (puzzle[large_pos.first][large_pos.second] != 0) {  // large_pos has been assigned
                for (int k = puzzle[large_pos.first][large_pos.second]; k <= size; k++) {
                    domains[small_pos.first][small_pos.second].erase(k);
                }
            }
            else {  // large_pos has not been assigned
                int minimum = *domains[small_pos.first][small_pos.second].begin();
                domains[large_pos.first][large_pos.second].erase(minimum);
            }
            if (puzzle[small_pos.first][small_pos.second] != 0) {
                for (int k = 1; k <= puzzle[small_pos.first][small_pos.second]; k++) {
                    domains[large_pos.first][large_pos.second].erase(k);
                }
            }
            else {
                int minimum = *domains[large_pos.first][large_pos.second].rbegin();
                domains[small_pos.first][small_pos.second].erase(minimum);
            }
        }
        new_domain_count = domainCount(domains);
    } while(old_domain_count == new_domain_count);

    return domains;
}

/*
    在每次赋值（即拓展一个节点后）更新值域。
    主要还是根据行列限制和小于限制。
    根据这个时间来计算表格第五列.
*/
vector<vector<set<int>>> Futoshiki::updateDomains(vector<vector<set<int>>> domains, const pair<int, int>& pos) {
    auto t1_per = steady_clock::now();
    // 检查同行是否有重复
    for (int i = 0; i < size; i++) {
        if (i == pos.first)
            continue;
        else if (puzzle[i][pos.second] == puzzle[pos.first][pos.second]) {
            return vector<vector<set<int>>>();  // DWO，其实这一段不太必要
        } else {
            domains[i][pos.second].erase(puzzle[pos.first][pos.second]);
            if (domains[i][pos.second].size() == 0) {
                return vector<vector<set<int>>>();  // DWO
            }
        }
    }

    // 检查同列是否有重复
    for (int j = 0; j < size; j++) {
        if (j == pos.second)
            continue;
        else if (puzzle[pos.first][j] == puzzle[pos.first][pos.second]) {
            return vector<vector<set<int>>>();  // DWO
        } else {
            domains[pos.first][j].erase(puzzle[pos.first][pos.second]);
            if (domains[pos.first][j].size() == 0) {
                return vector<vector<set<int>>>();  // DWO
            }
        }
    }

    // 小于限制
    for (int i = 0; i < con_num; i++) {
        pair<int, int> small_pos = constraints[i].first;
        pair<int, int> large_pos = constraints[i].second;
        if (pos == large_pos) {
            for (int k = puzzle[pos.first][pos.second]; k <= size; k++) {
                domains[small_pos.first][small_pos.second].erase(k);
                if (puzzle[small_pos.first][small_pos.second] == 0 && domains[small_pos.first][small_pos.second].size() == 0) {
                    return vector<vector<set<int>>>();  // DWO
                }
            }
        } else if (pos == small_pos) {
            for (int k = 1; k <= puzzle[pos.first][pos.second]; k++) {
                domains[large_pos.first][large_pos.second].erase(k);
                if (puzzle[large_pos.first][large_pos.second] == 0 && domains[large_pos.first][large_pos.second].size() == 0) {
                    return vector<vector<set<int>>>();  // DWO
                }
            }
        }
    }
    auto t2_per = steady_clock::now();
    duration<double> time_span_per = duration_cast<duration<double>>(t2_per - t1_per);
    sum_time += time_span_per.count();
    return domains;
}

/* 找到值域最小的点并返回以拓展之 */
pair<int, int> Futoshiki::mrv(const vector<vector<set<int>>>& domains) {
    int min_val = size * size;  // max size of domain
    pair<int, int> min_pos = make_pair(-1, -1);
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (puzzle[i][j] == 0 && domains[i][j].size() < min_val) {
                min_val = domains[i][j].size();
                min_pos = make_pair(i, j);
            }
        }
    }
    return min_pos;
}

/*  
    FC，赋值（即拓展节点）的过程在此
    根据MRV找到需要拓展的点，根据其值域遍历赋值
    然后递归
    若无解，最后要恢复
*/
vector<vector<int>> Futoshiki::forwardChecking(const vector<vector<set<int>>>& domains) {
    if (isSolved()) {
        return puzzle;
    }

    pair<int, int> pos = mrv(domains);

    for (auto pd = domains[pos.first][pos.second].begin(); pd != domains[pos.first][pos.second].end(); pd++) {
        puzzle[pos.first][pos.second] = *pd;                // 赋值
        num_of_nodes ++;
        auto temp_domains = updateDomains(domains, pos);    // 创建一个副本用来迭代
        if (temp_domains.size() != 0) {  // 非 DWO
            vector<vector<int>> ret = forwardChecking(temp_domains);
            if (ret.size() != 0) return ret;
        }
    }

    puzzle[pos.first][pos.second] = 0;  // 该情况无解，恢复到赋值以前的状态
    return vector<vector<int>>();
}

int main() {
    //Futoshiki game("puzzle1.txt", "constraints1.txt", 5, 7);
    //Futoshiki game("puzzle2.txt", "constraints2.txt", 6, 9);
    //Futoshiki game("puzzle3.txt", "constraints3.txt", 7, 19);
    Futoshiki game("puzzle4.txt", "constraints4.txt", 8, 25);
    //Futoshiki game("puzzle5.txt", "constraints5.txt", 9, 32);
    //后面两个数字代表题目的size和约束条件的个数，即class内定义的size和con_num。

    cout << "-----Initialization-----" << endl;
    for (int i = 0; i < game.size; i++) {
        for (int j = 0; j < game.size; j++) {
            cout << game.puzzle[i][j] << " ";
        }
        cout << endl;
    }

    auto domains = game.makeDomains();

    auto t1 = steady_clock::now();
    vector<vector<int>> result = game.forwardChecking(domains);
    auto t2 = steady_clock::now();
    duration<double> time_span = duration_cast<duration<double>>(t2 - t1);

    if (result.size() != 0) {
        cout << "-------Solution------" << endl;
        for (int i = 0; i < game.size; i++) {
            for (int j = 0; j < game.size; j++) {
                cout << result[i][j] << " ";
            }
            cout << endl;
        }
        cout << "------------------------Outcoming--------------------------" << endl;
        cout << "Run time is in FC :" << time_span.count()*1000 << "ms." << endl;
        cout << "Number of nodes in FC : " << num_of_nodes << "." << endl;
        cout << "Average time for constraint propagation : " << double(sum_time / num_of_nodes)*1000 << "ms." << endl;
        cout << "-----------------------------------------------------------" << endl;
    } else {
        cout << "No solution!" << endl;
    }
    return 0;
}