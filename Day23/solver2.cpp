#include <cstdio>
#include <iostream>

using namespace std;


struct mylist {
    mylist(int _val = -1, struct mylist* _prev = nullptr, struct mylist* _next = nullptr) : val(_val), prev(_prev), next(_next) {};
    int val;
    struct mylist *prev, *next;
};


void print_list(int round, mylist *head)
{
    cout << "[" << round << "] ";
    bool firstrun = true;
    for (mylist* curr = head; firstrun || curr != head; curr = curr->next) {
        cout << curr->val << " ";
        firstrun = false;
    }
    cout << endl;
}


int main()
{
    //int nums_len = 9;
    //int max_val = nums_len;
    //int nums[] = { 3, 8, 9, 1, 2, 5, 4, 6, 7 };   // example
    //int nums[] = { 9, 2, 5, 1, 7, 6, 8, 3, 4 };   // question 1
    
    int nums_len = 1000000;
    int max_val = nums_len;
    //int nums_9[] = { 3, 8, 9, 1, 2, 5, 4, 6, 7 };
    int nums_9[9] = { 9, 2, 5, 1, 7, 6, 8, 3, 4 };
    int *nums = new int[nums_len];
    for (int i = 0; i < nums_len; ++i) {
        nums[i] = (i < 9 ? nums_9[i] : i + 1);
    }

    mylist **numsmap = new mylist*[max_val + 1];

    mylist *head = new mylist(nums[0], nullptr, nullptr);
    mylist *prev = head;
    numsmap[nums[0]] = head;
    for (int i = 1; i < nums_len; ++i) {
        mylist *node = new mylist(nums[i], prev, nullptr);
        prev->next = node;
        numsmap[nums[i]] = node;

        prev = node;
    }
    head->prev = prev;
    prev->next = head;
    //print_list(0, head);

    mylist *curr = head;
    int max_round = 10000000;
    for (int round = 1; round <= max_round; ++round) {
        mylist* node1 = curr->next;
        mylist* node2 = node1->next;
        mylist* node3 = node2->next;
        
        int dst = curr->val;
        for (;;) {
            --dst;
            if (dst == node1->val || dst == node2->val || dst == node3->val) continue;
            if (dst == 0) {
                dst = max_val + 1;
                continue;
            }
            break;
        }

        // remove 3 nodes after current node
        node3->next->prev = curr;
        curr->next = node3->next;

        // insert 3 nodes after destination node
        mylist* node_dst = numsmap[dst];
        mylist* node_dst_next = node_dst->next;
        node_dst->next = node1;
        node1->prev = node_dst;
        node_dst_next->prev = node3;
        node3->next = node_dst_next;

        curr = curr->next;
        //print_list(round, curr);
    }

    mylist* nodeone = numsmap[1];
    long long ans = (long long)nodeone->next->val * (long long)nodeone->next->next->val;

    cout << "ans: " << ans << endl;

    return 0;
}
