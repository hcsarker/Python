/* 
 * Sample C test file for Compiler Design Sessional
 * Demonstrates comments, whitespace, keywords, identifiers,
 * operators, numbers (integer & float), and function structure.
 */

#include <stdio.h>

// Global variable definition
int max_limit = 100;

/* 
   Function: compute_sum
   Computes sum of numbers with discount factor
*/
float compute_sum(int count, float discount_rate) {
    float total = 0.0;
    int i = 1;

    while (i <= count) {
        if (i == 5) {
            total = total + (i * 0.5);
        } else {
            total = total + i;
        }
        i = i + 1;
    }

    float final_amount = total * (1.0 - discount_rate);
    return final_amount;
}

int main() {
    int n = 10;
    float rate = 0.15;
    float result = compute_sum(n, rate);

    // Print message with spaces that should be preserved inside string:
    char greeting[] = "Calculation successfully completed! Result: ";
    printf("%s %f\n", greeting, result);

    return 0;
}
