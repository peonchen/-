#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAX_SIZE 2048   // 内存块的最大大小
#define times 10        // 进程数量
#define sleep_time 2   // 进程执行时间
#define MAX_PCBZISE 200 // 进程控制块的最大大小

// 进程控制块
typedef struct PCB {
    int pid;    // 进程ID
    int size;   // 内存大小
} PCB;

// 内存块
typedef struct Block {
    int size;       // 内存块大小
    int start;      // 内存块起始地址
    int isFree;     // 是否空闲
    PCB* process;   // 指向进程控制块的指针
    struct Block* next; // 指向下一个内存块的指针
} Block;

// 伙伴结构
typedef struct Buddy {
    int size;           // 内存块大小
    Block* block;       // 指向内存块的指针
} Buddy;

// 初始化伙伴系统
void initBuddy(Buddy* buddy, int size) {
    buddy->size = MAX_SIZE;
    buddy->block = (Block*)malloc(sizeof(Block));
    if(buddy->block == NULL) {
        printf("内存分配失败");
        return;
    }
    buddy->block->next = NULL;
    buddy->block->start = 0;
    buddy->block->process = NULL;
    buddy ->block ->isFree = 1;
    buddy->block->size = size;
}
int splitBlock(Block* block){
    if(block->size == 1)
        return 0;
    int newSize = block->size / 2;
    Block* newBlock = (Block*)malloc(sizeof(Block));
    newBlock -> next = NULL;
    newBlock -> start = block->start + newSize;
    newBlock -> process = NULL;
    newBlock->size = newSize;
    newBlock->isFree = 1;
    block->size = newSize;
    if(block -> next != NULL){
        newBlock->next = block->next;
    }
    block->next = newBlock;
    return 1;
}
//合并内存
void mergeBlock(Buddy* buddy, Block* block) {
    if (block == NULL) {
        return;
    }

    int x = block->start;
    // 合并当前块和后一个块
    if (x % (block->size * 2) == 0) {
        Block* nextBlock = block->next;
        if (nextBlock != NULL && nextBlock->isFree == 1 && nextBlock->size == block -> size && nextBlock->start == block->start + block->size) {
            block->size *= 2;
            block->next = nextBlock->next;
            free(nextBlock);
            mergeBlock(buddy, block);
        }
    }else if(x % (block->size *2) == block->size) {
        // 合并当前块和前一个块
        Block* prevBlock = buddy->block;
        while (prevBlock != NULL && prevBlock->next != block) {
            prevBlock = prevBlock->next;
        }
        if (prevBlock != NULL && prevBlock->isFree == 1 && prevBlock->size == block->size && prevBlock->start + prevBlock->size == block->start) {
            prevBlock->size *= 2;
            prevBlock->next = block->next;
            free(block);
            mergeBlock(buddy, prevBlock);
        }
    }
}

//分配内存
void allocateMemory(Buddy* buddy,PCB *pcb) {
    Block* block = buddy->block;
    int powerPCB = 0;
    int powerBuffy = 0;
    while(pcb->size > block->size ||block ->isFree == 0){
        if(block->next == NULL){
            printf("内存不足");
            return;
        }
        block = block->next;
    }
    for(int i = 1; i < pcb->size; i = i * 2){
        powerPCB++;
    }
    for(int i = 1; i <block->size ; i = i * 2){
        powerBuffy++;
    }
    while(powerPCB < powerBuffy){
        if(splitBlock(block)){
            powerBuffy--;
        }
    }
    block->process = pcb;
    block->isFree = 0;
    }
void freeMemory(Buddy* buddy, PCB* pcb) {
    Block* block = buddy->block;
    // 找到对应进程的内存块
    while (block != NULL) {
        if (block->process == pcb) {
            block->isFree = 1;
            block->process = NULL;
            mergeBlock(buddy, block);
            return;
        }
        block = block->next;
    }
    printf("未找到对应的内存块\n");
}
void printBuddy(Buddy* buddy) {
    Block* block = buddy->block;
    printf("----------------------------------------------------------------------\n");
    printf("|  内存块起点  |  内存块大小  |  内存块状态  |  进程ID  |  进程大小  |\n");
    printf("----------------------------------------------------------------------\n");

    while (block != NULL) {
        if (block->isFree == 0) {
            printf("| %12d | %12d | %12d | %8d | %10d |\n", 
                   block->start, block->size, block->isFree, block->process->pid, block->process->size);
        } else {
            printf("| %12d | %12d | %12d |        - |          - |\n", 
                   block->start, block->size, block->isFree);
        }
        printf("----------------------------------------------------------------------\n");
        block = block->next;
    }
}
//延迟模拟
// int main() {
//     Buddy *buddy = (Buddy*)malloc(sizeof(Buddy));
//     initBuddy(buddy, MAX_SIZE);
//     char ch; 
//     PCB* pcbs[times];
//     for (int i = 0; i < times; i++) {
//         pcbs[i] = (PCB*)malloc(sizeof(PCB));
//         pcbs[i]->pid = i;
//         pcbs[i]->size = rand() % MAX_PCBZISE + 1;
//         printf("进程%d申请内存大小为%d\n", pcbs[i]->pid, pcbs[i]->size);
//         allocateMemory(buddy, pcbs[i]);
//     }
//     printBuddy(buddy);
//     printf("\n 按任一键继续......"); 
//     ch=getchar(); 
//     // 模拟释放一些进程的内存
//     for (int i = 0; i < times; i ++) {
//         sleep(sleep_time);
//         system("cls");
//         printf("释放进程%d的内存\n", pcbs[i]->pid);
//         freeMemory(buddy, pcbs[i]);
//         printBuddy(buddy);
//     }
//     return 0;
// }
//一条龙版本
int main() {
    Buddy *buddy = (Buddy*)malloc(sizeof(Buddy));
    initBuddy(buddy, MAX_SIZE);
    PCB* pcbs[times];
    for (int i = 0; i < times; i++) {
        pcbs[i] = (PCB*)malloc(sizeof(PCB));
        pcbs[i]->pid = i;
        pcbs[i]->size = rand() % 100 + 1;
        printf("进程%d申请内存大小为%d\n", pcbs[i]->pid, pcbs[i]->size);
        allocateMemory(buddy, pcbs[i]);
        printBuddy(buddy);
    }
    printBuddy(buddy);
    // 模拟释放一些进程的内存
    for (int i = 0; i < times; i ++) {
        printf("释放进程%d的内存\n", pcbs[i]->pid);
        freeMemory(buddy, pcbs[i]);
        printBuddy(buddy);
    }
    return 0;
}