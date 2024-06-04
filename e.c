#include "stdio.h"
#define MAX_N 4  //进程
#define MAX_M 3 //资源
int n=4,m=3;
int max[MAX_N][MAX_M]={{1,2,2},{6,2,3},{7,2,3},{9,3,4}};
int allocation[MAX_N][MAX_M]={{1,0,0},{2,0,1},{3,1,0},{2,1,1}};
int need[MAX_N][MAX_M]={{2,2,2},{1,0,2},{1,0,3},{4,2,0}};  
int available[MAX_M]={1,1,2};
int safe(){
    int work[MAX_M]={0};
    int finish[MAX_N]={0};
    for(int i = 0; i < n; i++){
        finish[i]=0;
    }
    for(int i = 0; i < m; i++){
        work[i]=available[i];
    }  
    int count = 0;
    while(count < n){
        int flag = 0;
        for(int i = 0; i < n; i++){
            if(finish[i]==0){
                int j;
                for(j = 0; j < m; j++){
                    printf("%d---%d\n",need[i][j],work[j]);
                    if(need[i][j]>work[j]){
                        break;
                    }
                }
                if(j == m){
                    for(int k = 0; k < m; k++){
                        work[k]+=allocation[i][k];
                    }
                    finish[i]=1;
                    count++;
                    flag = 1;
                }
            }
        }
        if(flag == 0){
            return 0; //不安全
        }
    }
    return 1; //安全
}

int main(){

    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            need[i][j]=max[i][j]-allocation[i][j];
        }
    }    
    if(safe()){
        printf("---系统是安全的\n");
    }else{
        printf("--系统是不安全的\n");
    }
    return 0;
}
    // int m, n;
    // printf("请输入资源数和进程数：\n");
    // scanf("%d %d",&m,&n);

    // int max[n][m];  // 注意这里交换了 n 和 m 的位置
    // int allocation[n][m];  // 注意这里交换了 n 和 m 的位置
    // int need[n][m];  // 注意这里交换了 n 和 m 的位置
    // int available[m];

    // for(int i = 0; i < n; i++){
    //     printf("请输入进程%d对资源的需求量：\n",i);
    //     for(int j = 0; j < m; j++){
    //         scanf("%d",&max[i][j]);
    //     }
    // }
    // for(int i = 0; i < n; i++){
    //     printf("请输入进程%d对资源的已分配量：\n",i);
    //     for(int j = 0; j < m; j++){
    //         scanf("%d",&allocation[i][j]);
    //     }
    // }
    // for(int i = 0; i < m; i++){
    //     printf("请输入资源%d的可用量：\n",i);
    //     scanf("%d",&available[i]);
    // }  
