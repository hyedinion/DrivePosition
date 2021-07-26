#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M_PI   3.14159265358979323846264338327950288
#define degToRad(angleInDegrees) ((angleInDegrees) * M_PI / 180.0)
#define radToDeg(angleInRadians) ((angleInRadians) * 180.0 / M_PI)

int main()
{
    tan(degToRad(10));

    return 0;
}