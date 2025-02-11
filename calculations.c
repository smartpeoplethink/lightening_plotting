// "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (use quotes)
//  cl calculations.cpp or cl /EHsc /Fecalculations.exe calculations.cpp /link User32.lib in some cases
// .\calculations.exe
//#include <stdio.h>

int main(void) {
    static int counter = 0;
    counter++;
    return counter;
}

int add(void){
    return 1+1;
}