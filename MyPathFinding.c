#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>
int min(int a, int b)
{
    return (a > b) ? b : a;
}

float heuristic(int x1, int y1, int x2, int y2){
    int d = 1;
    int d2 = 1;
    float dx = abs(x1 - x2);
    float dy = abs(y1 - y2);
    return d * (dx + dy) + (d2 - 2 * d) * min(dx, dy);
}
float move_cost(int x1, int y1, int x2, int y2){
    if(x1 == x2 || y1 == y2){
        return 1;
    }else{
        return 1.2;
    }
}
float get_dist(int x1, int y1, int x2, int y2){
    return sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2));
}

struct Node{
    int x;
    int y;
    float G;
    float F;
    int cameFrom;
};

struct Length{
    int openNodes;
    int closedNodes;
};

struct ReturnVals{
    int length;
    int **Path;
};

void free_mem(int **arr, int length){
    for(int i = 0; i < length; i++){
        free(arr[i]);   
    }
    free(arr);
}



void change_map(int **arr, int x, int y, int i){
    arr[x][y] = i;
}

struct ReturnVals _AStarSearch(int** map, int start[], int end[], int tileSize, bool allow_diagonal_movement, int min_dist, int can_move_on[], int amount_of_movement){
    struct Length lengths = {1, 0};
    
    start[0] = (int)round(start[0]/tileSize);
    start[1] = (int)round(start[1]/tileSize);
    end[0] = (int)round(end[0]/tileSize);
    end[1] = (int)round(end[1]/tileSize);

    struct Node *closedNodes = malloc(0 * sizeof(struct Node));
    
    struct Node startingNode = {start[0], start[1], 0, -heuristic(start[0], start[1], end[0], end[1])};
    
    struct Node *openNodes = malloc(1 * sizeof(struct Node));
    openNodes[0] = startingNode;

    int adjacent_squares[8][2] = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
    if(allow_diagonal_movement){
        int adjacent_squares[8][2] =  {{0, -1}, {0, 1}, {-1, 0}, {1, 0}, {-1, -1}, {-1, 1}, {1, -1}, {1, 1}};
    }else{
        int adjacent_squares[4][2] = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
    }

    int count = 0;
    while(lengths.openNodes > 0){
        count += 1;

        if(count > 1000){
            break;
        }
        
        int pos = 0;
        float current_fscore = 1863462912;
        for(int i=0; i < lengths.openNodes; i++){
            if(openNodes[i].F < current_fscore){
                current_fscore = openNodes[i].F;
                pos = i;
            }
        }

        // Check if we have reached the goal
        float dist = (float)get_dist(openNodes[pos].x, openNodes[pos].y, end[0], end[1]);
        if(dist <= min_dist/50){
            int i = 1;
            struct Node *atpointer = &openNodes[pos];

            struct ReturnVals returning = {};
            returning.Path = malloc(1 * sizeof(int*));
            

            returning.Path[0] = malloc(2 * sizeof(int));
            returning.Path[0][0] = openNodes[pos].x*tileSize;
            returning.Path[0][1] = openNodes[pos].y*tileSize;
            while(atpointer->x != startingNode.x || atpointer->y != startingNode.y){
                returning.Path = (int**)realloc(returning.Path, (i+1)*sizeof(int*));
                returning.Path[i] = (int*)malloc(2*sizeof(int));
                atpointer = &closedNodes[atpointer->cameFrom];
                //pointer = pointer

                returning.Path[i][0] = atpointer->x*tileSize;
                returning.Path[i][1] = atpointer->y*tileSize;
                i++;
                //printf("\n  %i, %i \n", atpointer->x*50, atpointer->y*50);
            }
            returning.length = i;


            free(openNodes);
            free(closedNodes);

            return returning;  // Done!
        }

        int i;
        if(allow_diagonal_movement){
            i = 8;
        }else{
            i = 4;
        }
        
        struct Node neighbours[i];
        for(int i2 = 0; i2 < i; i2++){ // Adjacent squaress
            int cur_x = openNodes[pos].x+adjacent_squares[i2][0];
            int cur_y = openNodes[pos].y+adjacent_squares[i2][1];
            struct Node node = {cur_x, cur_y, 0, heuristic(cur_x, cur_y, end[0], end[1])};
            neighbours[i2] = node;
        }


        closedNodes = realloc(closedNodes, (lengths.closedNodes+1)*sizeof(struct Node));
        int temp_int = lengths.closedNodes;
        closedNodes[lengths.closedNodes] = openNodes[pos];

        lengths.closedNodes++;


        for(int i = pos; i < lengths.openNodes; i++)
        {
            openNodes[i] = openNodes[i + 1];
        }
        openNodes = realloc(openNodes, (lengths.openNodes-1)*sizeof(struct Node));
        lengths.openNodes--;

        // Update scores for vertices near the openNodes[pos] position
        for(int i2 = 0; i2 < i; i2++){
            
            if(neighbours[i2].x < 0 || neighbours[i2].y < 0 || neighbours[i2].x > 100 || neighbours[i2].y > 100){
                continue;
            }

            for(int i3 = 0; i3 < lengths.closedNodes; i3++){
                if(neighbours[i2].x == closedNodes[i3].x && neighbours[i2].y == closedNodes[i3].y){
                    continue;  // We have already processed this node exhaustively
                }
            }


            bool can_move = false;
            for(int i=0; i<amount_of_movement; i++){
                if(map[neighbours[i2].x][neighbours[i2].y] == can_move_on[i])
                {
                    can_move = true;
                }
            }

            if(!can_move)
            {
                continue;
            }



            bool inOpenNodes = false;
            for(int i = 0; i < lengths.openNodes; i++)
            {
                if(neighbours[i2].x == openNodes[i].x && neighbours[i2].y == openNodes[i].y){
                    inOpenNodes = true;
                    break;
                }
            }
            float candidate_g = openNodes[pos].G + move_cost(openNodes[pos].x, openNodes[pos].y, neighbours[i2].x, neighbours[i2].y);

            if(!inOpenNodes){
                openNodes = realloc(openNodes, (lengths.openNodes+1)*sizeof(struct Node));
                openNodes[lengths.openNodes] = neighbours[i2];
                lengths.openNodes++;
                        
            }else if(candidate_g >= neighbours[i2].G){
                continue;
            }
            openNodes[lengths.openNodes-1].cameFrom = temp_int;
            openNodes[lengths.openNodes-1].G = candidate_g;
            float h = heuristic(neighbours[i2].x, neighbours[i2].y, end[0], end[1]);
            openNodes[lengths.openNodes-1].F = candidate_g+h;
            //printf("DEDENEJDE     %i    %i\n", openNodes[lengths.openNodes-1].x, openNodes[lengths.openNodes-1].y);
        }
    }

    
    struct ReturnVals returning = {};
    returning.length = 0;
    free(openNodes);
    free(closedNodes);

    return returning; 
}

int** create_Map(int x, int y)
{
    int **map;
    map = malloc(x * sizeof(int *));
    for(int i2 = 0; i2 < x; i2++){
        map[i2] = malloc(y * sizeof(int));
        for(int ii = 0; ii < y; ii++)
        {
            map[i2][ii] = 0;
        }
    }   
    return map;
}

int main()
{
    int** map = create_Map(100, 100);
    for(int i=0; i<1; i++){
        int start[2] = {1000, 1000};
        int end[2] = {4950, 1400};
        int arr[3] = {0};
        struct ReturnVals c = _AStarSearch(map, start, end, 50, true, 1, arr, 1);
        for(int i=0; i<c.length; i++)
        {
            printf("%i, %i \n", c.Path[i][0], c.Path[i][1]);
        }
        free_mem(c.Path, c.length);
    }
    return 0;
}

struct Len{
    int i;
    int i2;
};

int test()
{
    return 1;
}