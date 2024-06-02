#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 4096
#define times 10

// ���̿��ƿ�
typedef struct PCB {
    int pid;    // ����ID
    int size;   // �ڴ��С
    int status; // ����״̬���������С������ȣ�
    int super;
    int ntime;
    int rtime;
} PCB;

// �ڴ��
typedef struct Block {
    int size;       // �ڴ���С
    int start;      // �ڴ����ʼ��ַ
    int isFree;     // �Ƿ����
    PCB* process;   // ָ����̿��ƿ��ָ��
    struct Block* next; // ָ����һ���ڴ���ָ��
} Block;

// ���ṹ
typedef struct Buddy {
    int size;           // �ڴ���С
    Block* block;       // ָ���ڴ���ָ��
} Buddy;

// ��ʼ�����ϵͳ
void initBuddy(Buddy* buddy, int size) {
    buddy->size = MAX_SIZE;
    buddy->block = (Block*)malloc(sizeof(Block));
    if(buddy->block == NULL) {
        printf("�ڴ����ʧ��");
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
//�ϲ��ڴ�
void mergeBlock(Buddy* buddy, Block* block) {
    if (block == NULL) {
        return;
    }

    int x = block->start;
    // �ϲ���ǰ��ͺ�һ����
    if (x % (block->size * 2) == 0) {
        Block* nextBlock = block->next;
        if (nextBlock != NULL && nextBlock->isFree == 1 && nextBlock->size == block -> size && nextBlock->start == block->start + block->size) {
            block->size *= 2;
            block->next = nextBlock->next;
            free(nextBlock);
            mergeBlock(buddy, block);
        }
    } else {
        // �ϲ���ǰ���ǰһ����
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

//�����ڴ�
void allocateMemory(Buddy* buddy,PCB *pcb) {
    Block* block = buddy->block;
    int powerPCB = 0;
    int powerBuffy = 0;
    while(pcb->size > block->size ||block ->isFree == 0){
        if(block->next == NULL){
            printf("�ڴ治��");
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
    // �ҵ���Ӧ���̵��ڴ��
    while (block != NULL) {
        if (block->process == pcb) {
            block->isFree = 1;
            block->process = NULL;
            mergeBlock(buddy, block);
            return;
        }
        block = block->next;
    }
    printf("δ�ҵ���Ӧ���ڴ��\n");
}
void printBuddy(Buddy* buddy) {
    Block*block = buddy->block;
    while(block != NULL){
        
        if(block ->isFree == 0){
            printf("�ڴ���СΪ%d,�ڴ�����Ϊ%d,�ڴ��״̬Ϊ%d", block->size,block->start,block->isFree);
            printf("����IDΪ%d,���̴�С%d\n",block->process->pid,block->process->size);
        }
        else{
            printf("�ڴ���СΪ%d,�ڴ�����Ϊ%d,�ڴ��״̬Ϊ%d\n", block->size,block->start,block->isFree);
        }
        block = block->next;
    }
    return 0;
}
int main() {
    Buddy *buddy = (Buddy*)malloc(sizeof(Buddy));
    initBuddy(buddy, MAX_SIZE);
    PCB* pcbs[times];
    for (int i = 0; i < times; i++) {
        pcbs[i] = (PCB*)malloc(sizeof(PCB));
        pcbs[i]->pid = i;
        pcbs[i]->size = rand() % 100 + 1;
        pcbs[i]->status = 1;
        pcbs[i]->super = rand() % 5 + 1;
        pcbs[i]->ntime = rand() % 7 + 1;
        printf("����%d�����ڴ��СΪ%d\n", pcbs[i]->pid, pcbs[i]->size);
        allocateMemory(buddy, pcbs[i]);
    }
    printBuddy(buddy);
    // ģ���ͷ�һЩ���̵��ڴ�
    for (int i = 0; i < times; i ++) {
        printf("�ͷŽ���%d���ڴ�\n", pcbs[i]->pid);
        freeMemory(buddy, pcbs[i]);
        printBuddy(buddy);
    }
    return 0;
}
