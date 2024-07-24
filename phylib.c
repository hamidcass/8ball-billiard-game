#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "phylib.h"

phylib_object *phylib_new_still_ball(unsigned char number,
                                     phylib_coord *pos)
{

    phylib_object *newObj = malloc(sizeof(phylib_object));

    // malloc failed
    if (newObj == NULL)
    {
        return NULL;
    }
    else
    {
        newObj->type = PHYLIB_STILL_BALL;
        newObj->obj.still_ball.number = number;
        newObj->obj.still_ball.pos = *pos;
    }

    return newObj;
}

phylib_object *phylib_new_rolling_ball(unsigned char number,
                                       phylib_coord *pos,
                                       phylib_coord *vel,
                                       phylib_coord *acc)
{
    phylib_object *newObj = malloc(sizeof(phylib_object));

    // malloc failed
    if (newObj == NULL)
    {
        return NULL;
    }
    else
    {
        newObj->type = PHYLIB_ROLLING_BALL;
        newObj->obj.rolling_ball.number = number;
        newObj->obj.rolling_ball.pos = *pos;
        newObj->obj.rolling_ball.vel = *vel;
        newObj->obj.rolling_ball.acc = *acc;
    }

    return newObj;
}

phylib_object *phylib_new_hole(phylib_coord *pos)
{
    phylib_object *newObj = malloc(sizeof(phylib_object));

    // malloc failed
    if (newObj == NULL)
    {
        return NULL;
    }
    else
    {
        newObj->type = PHYLIB_HOLE;
        newObj->obj.hole.pos = *pos;
    }

    return newObj;
}

phylib_object *phylib_new_hcushion(double y)
{
    phylib_object *newObj = malloc(sizeof(phylib_object));

    // malloc failed
    if (newObj == NULL)
    {
        return NULL;
    }
    else
    {
        newObj->type = PHYLIB_HCUSHION;
        newObj->obj.hcushion.y = y;
    }

    return newObj;
}

phylib_object *phylib_new_vcushion(double x)
{
    phylib_object *newObj = malloc(sizeof(phylib_object));

    // malloc failed
    if (newObj == NULL)
    {
        return NULL;
    }
    else
    {
        newObj->type = PHYLIB_VCUSHION;
        newObj->obj.vcushion.x = x;
    }

    return newObj;
}

phylib_table *phylib_new_table(void)
{
    phylib_table *newTable = malloc(sizeof(phylib_table));

    if (newTable == NULL)
    {
        return NULL;
    }

    newTable->time = 0.0;
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // add 6 holes to obj list
    newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    newTable->object[5] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});
    newTable->object[8] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH / 2});
    newTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2});

    // set remaining pointers to null
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
    {

        newTable->object[i] = NULL;
    }

    return newTable;
}

void phylib_copy_object(phylib_object **dest, phylib_object **src)
{

    phylib_object *newObj = malloc(sizeof(phylib_object));

    if (newObj != NULL)
    {

        memcpy(newObj, *src, sizeof(phylib_object));

        if (*src == NULL)
        {
            *dest = NULL;
        }
        else
        {
            // saving address of object
            *dest = newObj;
        }
    }
}

phylib_table *phylib_copy_table(phylib_table *table)
{

    phylib_table *newTable = malloc(sizeof(phylib_table));
    if (newTable == NULL)
    {
        return NULL;
    }
    else
    {
        memcpy(newTable, table, sizeof(phylib_table));

        newTable->time = table->time;

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if (table->object[i] != NULL)
            {
                phylib_copy_object(&newTable->object[i], &table->object[i]);
            }
        }

        return newTable;
    }
}

void phylib_add_object(phylib_table *table, phylib_object *object)
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {

        if (table->object[i] == NULL)
        {

            // printf("Size of *object = %lu\nSize of object = %lu\n\nSize of phylib_object = %lu\n", sizeof(*object), sizeof(object), sizeof(phylib_object));
            //  memcpy(table->object[i], object, sizeof(phylib_object));
            table->object[i] = object;
            break;
        }
    }
}

void phylib_free_table(phylib_table *table)
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
        }
    }
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    phylib_coord newCoord;
    newCoord.x = (c1.x) - (c2.x);
    newCoord.y = (c1.y) - (c2.y);
    return newCoord;
}

double phylib_length(phylib_coord c)
{
    return sqrt(((c.x) * (c.x)) + ((c.y) * (c.y)));
}

double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    return (a.x * b.x) + (a.y * b.y);
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{
    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1;
    }
    else
    { // object 1 is a rolling ball
        // get distance
        if (obj2->type == PHYLIB_ROLLING_BALL || obj2->type == PHYLIB_STILL_BALL)
        {

            // distance is calculated: √((x2-x1)+(y2-y1))
            if (obj2->type == PHYLIB_STILL_BALL)
            {
                // printf("RB: X:%f  Y:%f\n", );
                // printf("SB: X:%f  Y:%f\n");
                double xdist = (obj2->obj.still_ball.pos.x) - (obj1->obj.rolling_ball.pos.x);
                double ydist = (obj2->obj.still_ball.pos.y) - (obj1->obj.rolling_ball.pos.y);
                double totalDist = (sqrt(xdist * xdist + ydist * ydist)) - PHYLIB_BALL_DIAMETER;
                return totalDist;
            }
            else // obj2 is rolling
            {
                double xdist = (obj2->obj.rolling_ball.pos.x) - (obj1->obj.rolling_ball.pos.x);
                double ydist = (obj2->obj.rolling_ball.pos.y) - (obj1->obj.rolling_ball.pos.y);
                double totalDist = (sqrt(xdist * xdist + ydist * ydist)) - PHYLIB_BALL_DIAMETER;

                // printf("xdist: %f\n", xdist);
                // printf("ydist = %f\n", ydist);

                return totalDist;
            }
        }
        else if (obj2->type == PHYLIB_HOLE)
        {

            double xdist = (obj2->obj.hole.pos.x) - (obj1->obj.rolling_ball.pos.x);

            double ydist = (obj2->obj.hole.pos.y) - (obj1->obj.rolling_ball.pos.y);

            double totalDist = (sqrt(xdist * xdist + ydist * ydist)) - PHYLIB_HOLE_RADIUS;

            return totalDist;
        }
        // test the cushion part because i dont know if im calculating this correctly
        else if (obj2->type == PHYLIB_HCUSHION)
        {
            double xdist = (obj2->obj.hcushion.y) - (obj1->obj.rolling_ball.pos.y);
            return fabs(xdist) - PHYLIB_BALL_RADIUS;
        }
        else if (obj2->type == PHYLIB_VCUSHION)
        {
            double ydist = (obj2->obj.vcushion.x) - (obj1->obj.rolling_ball.pos.x);

            return fabs(ydist) - PHYLIB_BALL_RADIUS;
        }

        else
        {
            return -1;
        }
    }
}

// part 3 functions

// updates existing object to after it has rolled
void phylib_roll(phylib_object *new, phylib_object *old, double time)
{
    if (new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL)
    {
        // update values in ball (old to new)

        // x values:
        new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + ((old->obj.rolling_ball.vel.x) * (time)) + (0.5 * (old->obj.rolling_ball.acc.x) * (time * time));

        // y values
        new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + ((old->obj.rolling_ball.vel.y) * (time)) + (0.5 * (old->obj.rolling_ball.acc.y) * (time * time));

        double oldVelX, oldVelY;
        oldVelX = old->obj.rolling_ball.vel.x;
        oldVelY = old->obj.rolling_ball.vel.y;

        // update velocity:
        new->obj.rolling_ball.vel.x = oldVelX + (old->obj.rolling_ball.acc.x) * (time);
        new->obj.rolling_ball.vel.y = oldVelY + (old->obj.rolling_ball.acc.y) * (time);

        // if either velocity changes sign
        if (oldVelX * new->obj.rolling_ball.vel.x < 0)
        {

            new->obj.rolling_ball.vel.x = 0;
            // new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.x = 0;
        }
        if (oldVelY * new->obj.rolling_ball.vel.y < 0)
        {

            // new->obj.rolling_ball.vel.x = 0;

            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }
    }
}

unsigned char phylib_stopped(phylib_object *object)
{

    // if (object->obj.rolling_ball.acc.y == 0 && object->obj.rolling_ball.acc.x == 0)
    // {
    //     return 1;
    // }

    // printf("%f\n", phylib_length(object->obj.rolling_ball.vel));
    if (phylib_length(object->obj.rolling_ball.vel) < 0.1)
    {

        // printf("%f\n", phylib_length(object->obj.rolling_ball.vel));
        object->type = PHYLIB_STILL_BALL;

        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;

        // object = phylib_new_still_ball(object->obj.rolling_ball.number, &(object->obj.rolling_ball.pos));

        return 1;
    }
    else
    {
        return 0;
    }
}

void phylib_bounce(phylib_object **a, phylib_object **b)
{
    // assume object a is a rolling ball

    phylib_coord r_ab;
    phylib_object *prev;

    // printf("object hit was type %d\n", (*b)->type);

    switch ((*b)->type)
    {
    case PHYLIB_HCUSHION:
        // printf("ball hit a horizontal pad!\n");
        (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
        (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_VCUSHION:
        // printf("ball hit a vertical pad!\n");
        (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
        (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
        break;
    case PHYLIB_HOLE:
        // printf("Ball hit a hole\n");
        free((*a));
        (*a) = NULL;

        break;
    case PHYLIB_STILL_BALL:
        // printf("Hit a still ball\n");
        prev = *b;

        phylib_coord pos = (*b)->obj.rolling_ball.pos;
        phylib_coord vel = {0, 0};
        phylib_coord acc = {0, 0};
        unsigned char number = (*b)->obj.still_ball.number;

        (*b) = phylib_new_rolling_ball(number, &pos, &vel, &acc);
        free(prev);

        //(*b)->type = PHYLIB_ROLLING_BALL;

    case PHYLIB_ROLLING_BALL:

        // position of a from b

        r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

        // relative velocity of a w/ respect to b
        phylib_coord v_rel;
        v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

        // calculate normal vector
        phylib_coord n;
        n.x = r_ab.x / phylib_length(r_ab);
        n.y = r_ab.y / phylib_length(r_ab);

        // ratio
        double v_rel_n;
        v_rel_n = phylib_dot_product(v_rel, n);

        // update ball a
        // x vel:
        (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
        // y vel:
        (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y);

        // update ball b:

        (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
        (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

        // printf(" subtract from velo: %f\n", v_rel_n * n.y);

        // calculate speed of both balls:

        // a:
        double speedA = phylib_length((*a)->obj.rolling_ball.vel);
        double speedB = phylib_length((*b)->obj.rolling_ball.vel);

        if (speedA > PHYLIB_VEL_EPSILON)
        {

            (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speedA * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speedA * PHYLIB_DRAG;
        }

        if (speedB > PHYLIB_VEL_EPSILON)
        {

            (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x) / speedB * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y) / speedB * PHYLIB_DRAG;
        }

        // printf("Vel of ball: X:%f\nY:%f\n", (*a)->obj.rolling_ball.vel.x, (*a)->obj.rolling_ball.vel.y);

        break;
    default:
        break;
    }
}

unsigned char phylib_rolling(phylib_table *t)
{
    int counter = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (t->object[i] != NULL)
        {
            if (t->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                counter++;
            }
        }
    }
    return counter;
}

phylib_table *phylib_segment(phylib_table *table)
{

    if (!(phylib_rolling(table))) // no rolling balls
    {
        return NULL;
    }
    else // rolling balls exist
    {
        // make copy of table
        phylib_table *newTable = phylib_copy_table(table);

        double simTime = PHYLIB_SIM_RATE;

        while (simTime < PHYLIB_MAX_TIME)
        {
            // printf("Time : %f\n", simTime);

            // search for all rolling balls
            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
            {
                if (newTable->object[i] != NULL &&
                    newTable->object[i]->type == PHYLIB_ROLLING_BALL)
                {

                    phylib_roll(newTable->object[i], table->object[i], simTime);

                    // check if ball stopped

                    if (phylib_stopped(newTable->object[i]))
                    {

                        // printf("Time: %f\n", newTable->time + simTime);
                        newTable->time += simTime;
                        return newTable;
                    }
                    // printf("rolled\n");
                }
            }

            for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
            {
                if (newTable->object[i] != NULL &&
                    newTable->object[i]->type == PHYLIB_ROLLING_BALL)
                {

                    // check if ball hits another object
                    for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)

                    {
                        // check for bounce
                        if (newTable->object[j] != NULL &&
                            i != j &&
                            phylib_distance(newTable->object[i], newTable->object[j]) < 0)
                        {
                            // printf("Distance: %f\n", phylib_distance(newTable->object[i], newTable->object[j]));
                            // printf("T: %f\n", simTime);
                            // printf("Before: Y: %f\n", newTable->object[i]->obj.rolling_ball.vel.y);
                            phylib_bounce(&newTable->object[i], &newTable->object[j]);
                            // printf("After: Y: %f\n", newTable->object[i]->obj.rolling_ball.vel.y);

                            // printf("Bounce! ball [%d] hit [%d]\n", i, j);
                            newTable->time += simTime;

                            return newTable;
                        }
                    }
                }
            }

            simTime += PHYLIB_SIM_RATE;
        }

        return newTable;
    }
}

char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
    }
    return string;
}
