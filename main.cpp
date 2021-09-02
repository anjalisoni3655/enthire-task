#include <bits/stdc++.h>
using namespace std;

void printPathsUtil(vector<vector<int>> paths, int currentNode,
                    vector<vector<int>> &ans, vector<int> &currentPath)
{

  currentPath.push_back(currentNode);

  if (currentNode == paths.size() - 1)
  {
    ans.push_back(currentPath);
  }
  else
  {
    for (int j = 0; j < paths[currentNode].size(); j++)
    {

      printPathsUtil(paths, paths[currentNode][j], ans, currentPath);
    }
  }
  currentPath.pop_back(); //back track
}

vector<vector<int>> printPaths(vector<vector<int>> paths)
{

  vector<vector<int>> ans;
  vector<int> currentPath;

  printPathsUtil(paths, 0, ans, currentPath);
  return ans;
}

int main()
{
  //[[4,3,1],[3,2,4],[3],[4],[]]
  vector<vector<int>> paths = {{4, 3, 1}, {3, 2, 4}, {3}, {4}, {}};
  vector<vector<int>> ans = printPaths(paths);
  for (int i = 0; i < ans.size(); i++)
  {
    for (int j = 0; j < ans[i].size(); j++)
    {
      cout << ans[i][j] << " ";
    }
    cout << "\n";
  }
}
