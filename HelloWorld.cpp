#include <iostream>
#include <vector>
#include <windows.h>
#include <cstdio>
// 计算阶乘函数
unsigned long long factorial(int n)
{
    if (n < 0)
    {
        std::cout << "阶乘只适用于非负整数！" << std::endl;
        return 0;
    }

    unsigned long long result = 1;
    for (int i = 1; i <= n; ++i)
    {
        result *= i;
    }
    return result;
}

// 打印向量内容
void printVector(const std::vector<int> &v)
{
    std::cout << "向量内容: ";
    for (int val : v)
    {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}

int main()
{
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    int n;
    std::cout << "请输入一个整数: ";
    std::cin >> n;

    // 计算阶乘
    unsigned long long fact = factorial(n);
    std::cout << n << " 的阶乘是: " << fact << std::endl;

    // 使用 vector 示例
    std::vector<int> numbers;
    for (int i = 1; i <= n; ++i)
    {
        numbers.push_back(i);
    }
    printVector(numbers);
    system("pause");
    // std::cin.get(); // 等待回车
    return 0;
}
