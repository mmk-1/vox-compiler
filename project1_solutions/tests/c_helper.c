#include "c_helper.h"
#include <stdio.h>
#include <stdlib.h>


void __print_helper__(long argc){
  printf("%d\n", argc);
}

void __vector_print__(long argc[]){
    long * vector = argc;
    long length = vector[0];

    putchar('[');
    for(long i = 1; i <= length; i++) printf("%d, ", vector[i]);
    printf("]\n");
}

void __string_print__(long argc[]){
    long * vector = argc;
    long length = vector[0];

    for(long i = 1; i <= length; i++) printf("%c", vector[i]);
    printf("\n");
}

long * __init_string__(long argc,  long argv[]){
  long* vector = (long* )malloc((argc+1)*sizeof(long));
  vector[0] = argc;

  for(long i = 1; i < argc+1; i++){
    vector[i] = argv[i-1]; 
  }
  
  return vector;
}

long * __v_add__(long argc, long argv1[], long argv2[]){
    long* vector1 = argv1;
    long* vector2 = argv2;

    if(vector1[0] != vector2[0]){
    puts("Vector sizes do not match.");
    exit(1);
    }

    long* result_vector = (long* )malloc((vector1[0]+1)*sizeof(long));
    result_vector[0] = vector1[0];
    _vv_add(vector1+1, vector2+1, result_vector+1, vector1[0]);

    return result_vector;
}


