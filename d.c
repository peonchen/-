#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 4096

// 进程控制块
typedef struct PCB {
    int pid;    // 进程ID
    int size;   // 内存大小
    int status; // 进程状态（比如运行、阻塞等）
    int super;
    int ntime;
    int rtime;
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
    int x = block->start;
    if(x % (block->size * 2) == 0){
        Block* nextBlock = block->next;
        if(nextBlock->isFree == 1){
            
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
int main() {
    Buddy *buddy = (Buddy*)malloc(sizeof(Buddy));
    initBuddy(buddy, MAX_SIZE);
    for(int i = 0; i < 15; i++){
        PCB* pcb = (PCB*)malloc(sizeof(PCB));
        pcb -> pid = i;
        pcb->size = rand() % 100 + 1;
        pcb->status = 1;
        pcb->super = rand() % 5 + 1;
        pcb->ntime = rand() % 7 + 1;
        printf("进程%d申请内存大小为%d\n", pcb->pid, pcb->size);
        allocateMemory(buddy,pcb);
    }
    printf("OK");
    Block*block = buddy->block;
    while(block != NULL){
        
        if(block ->isFree == 0){
            printf("内存块大小为%d,内存块起点为%d,内存块状态为%d", block->size,block->start,block->isFree);
            printf("进程ID为%d,进程大小%d\n",block->process->pid,block->process->size);
        }
        else{
            printf("内存块大小为%d,内存块起点为%d,内存块状态为%d\n", block->size,block->start,block->isFree);
        }
        block = block->next;
    }
    return 0;
}
