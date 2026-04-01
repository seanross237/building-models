# Logic/Reasoning Questions — BBEH

Source: BIG-Bench Extra Hard (BBEH). Designed to be hard for LLMs.

---

## LOGIC-01: Novel Arithmetic Operators
**Domain:** Arithmetic / Symbolic Computation
**Type:** exactMatch

Consider the following new operations:

$a ! b$ equals $(a + b)$ if $a - b > 0$; otherwise,  it equals $a * b$.
$a : b$ equals $(a * b)$ if $a - b > 0$; otherwise,  it equals $-a * -b$.
$a ~ b$ equals $(b : a) - b$ if $|a-b| < 2$ and $(a : b) - a$ otherwise.
$a # b$ equals $(a ~ a) ! b$ if $b < 2$ and $(b ~ b) ! a$ otherwise.
$a <> b$ equals $a # b$ if $gcd(a, b) == 1$ and $gcd(a, b)$ otherwise, where gcd stands for greatest common divisor.
$a ][ b$ equals $min(a, b)$ if either $a$ or $b$ is prime and $max(a, b)$ otherwise.
For brevity, we use $a <op1><op2> b$ to denote $(a op1 b) op2 b$. For example, $4 +* -5$ means $(4 + -5) * -5$ and $4 *-- -5$ means $(4 * -5) -- -5$.
Let A = ((((-10 -! ten) - (-6 #<> 10)) #*- ((-1 # -2) ][][ (seven ! -7))) ][ (((-2 ! -10) -* (-8 ~!+ -7)) #* ((nine *!! -2) *+<> (eight <> -2))))
Let B = ((((-6 ][+ -3) - (-1 # -7)) -*<> ((-10 ! -6) <> (-6 : one))) * (((1 <> seven) -# (eight ][-* eight)) ][ ((-8 +:: 1) : (six #+ one))))
Let C = ((((2 ! -3) #- (-4 +:~ -5)) :*# ((4 -<> four) # (5 # 2))) <> (((8 : -10) ][:! (2 **<> -1)) ][ ((-6 +! -4) - (4 * eight)))).
Compute A + B - C. Your final answer must be in number form.

---

## LOGIC-02: Board Game Rule Chaining
**Domain:** Logical Deduction / Rule-Based Reasoning
**Type:** exactMatch

A few players are playing a boardgame. The current state of the game is as follows. The beetle has 81 dollars. The beetle has a card that is red in color. The camel has a card that is blue in color, and is a software developer. The coyote has a knapsack. The dinosaur pays money to the gorilla. The dolphin brings an oil tank for the peafowl. The lizard has 34 dollars. The pelikan is currently in Peru. The reindeer has a basketball with a diameter of 20 inches. The swallow shouts at the seahorse. The vampire shouts at the monkey. The walrus has some arugula. The wolf has 48 dollars. And the rules of the game are as follows. Rule1: If there is evidence that one animal, no matter which one, manages to persuade the zebra, then the bee enjoys the companionship of the finch undoubtedly. Rule2: The camel will not neglect the bear if it (the camel) works in computer science and engineering. Rule3: There exists an animal which refuses to help the cobra? Then the swallow definitely invests in the company owned by the mermaid. Rule4: If at least one animal borrows a weapon from the worm, then the flamingo hugs the chihuahua. Rule5: The living creature that invests in the company whose owner is the mule will also destroy the wall constructed by the pigeon, without a doubt. Rule6: If the walrus dances with the camel, then the camel is not going to leave the houses that are occupied by the rhino. Rule7: If the akita does not hug the swan, then the swan does not reveal a secret to the woodpecker. Rule8: There exists an animal which enjoys the company of the finch? Then the goat definitely surrenders to the finch. Rule9: If you are positive that you saw one of the animals pays money to the gorilla, you can be certain that it will also refuse to help the cobra. Rule10: If the mannikin does not shout at the butterfly but the zebra suspects the truthfulness of the butterfly, then the butterfly reveals a secret to the fish unavoidably. Rule11: If something does not want to see the frog, then it does not shout at the butterfly. Rule12: If the coyote does not pay some $$$ to the dalmatian, then the dalmatian does not negotiate a deal with the dugong. Rule13: One of the rules of the game is that if the mermaid surrenders to the swan, then the swan will, without hesitation, reveal something that is supposed to be a secret to the woodpecker. Rule14: The coyote will not pay money to the dalmatian if it (the coyote) has something to carry apples and oranges. Rule15: The camel will not neglect the bear if it (the camel) has a card whose color starts with the letter "l". Rule16: The mermaid unquestionably surrenders to the swan, in the case where the pelikan calls the mermaid. Rule17: The bee does not invest in the company owned by the mule, in the case where the crab unites with the bee. Rule18: If there is evidence that one animal, no matter which one, brings an oil tank for the peafowl, then the poodle manages to persuade the zebra undoubtedly. Rule19: If there is evidence that one animal, no matter which one, pays some $$$ to the mouse, then the goat is not going to disarm the liger. Rule20: If at least one animal shouts at the monkey, then the ant does not hug the dalmatian. Rule21: If something does not dance with the husky and additionally not negotiate a deal with the ant, then it will not want to see the frog. Rule22: From observing that one animal hides her cards from the rhino, one can conclude that it also swims in the pool next to the house of the bison, undoubtedly. Rule23: The living creature that surrenders to the finch will never enjoy the company of the dove. Rule24: If the walrus has a leafy green vegetable, then the walrus dances with the camel. Rule25: The poodle will not manage to persuade the zebra if it (the poodle) works in healthcare. Rule26: From observing that an animal does not create a castle for the goat, one can conclude that it pays money to the mouse. Rule27: The dalmatian unquestionably negotiates a deal with the dugong, in the case where the ant does not hug the dalmatian. Rule28: If there is evidence that one animal, no matter which one, smiles at the gadwall, then the mannikin is not going to negotiate a deal with the ant. Rule29: If the beetle has more money than the wolf and the lizard combined, then the beetle does not create one castle for the goat. Rule30: One of the rules of the game is that if the swan reveals a secret to the woodpecker, then the woodpecker will, without hesitation, borrow a weapon from the worm. Rule31: If you are positive that one of the animals does not disarm the liger, you can be certain that it will enjoy the company of the dove without a doubt. Rule32: The dugong does not acquire a photo of the cougar whenever at least one animal surrenders to the shark. Rule33: The mannikin does not dance with the husky, in the case where the owl stops the victory of the mannikin. Rule34: The living creature that disarms the llama will also call the mermaid, without a doubt. Rule35: The dugong unquestionably acquires a photo of the cougar, in the case where the dalmatian negotiates a deal with the dugong. Rule36: Regarding the beetle, if it has a card whose color starts with the letter "r", then we can conclude that it does not create a castle for the goat. Rule37: The pelikan will disarm the llama if it (the pelikan) is in South America at the moment. Rule38: There exists an animal which destroys the wall built by the pigeon? Then the zebra definitely suspects the truthfulness of the butterfly. Rule39: If there is evidence that one animal, no matter which one, leaves the houses that are occupied by the beaver, then the dinosaur is not going to refuse to help the cobra. Rule40: If at least one animal enjoys the company of the dove, then the bee invests in the company owned by the mule. Rule41: If you are positive that one of the animals does not neglect the bear, you can be certain that it will leave the houses occupied by the rhino without a doubt. Rule42: If the reindeer has a basketball that fits in a 23.5 x 30.6 x 23.6 inches box, then the reindeer does not hug the bee. Rule43: There exists an animal which acquires a photo of the cougar? Then the songbird definitely smiles at the gadwall. Rule44: The owl stops the victory of the mannikin whenever at least one animal swims in the pool next to the house of the bison. Rule45: The living creature that does not trade one of the pieces in its possession with the leopard will never swim in the pool next to the house of the bison. Rule17 is preferred over Rule40. Rule25 is preferred over Rule18. Rule27 is preferred over Rule12. Rule31 is preferred over Rule23. Rule32 is preferred over Rule35. Rule39 is preferred over Rule9. Rule41 is preferred over Rule6. Rule45 is preferred over Rule22. Rule7 is preferred over Rule13. A rule is only applicable if all of its antecedents can be proved. If a rule is preferred over the other, it means whenever both of them can be applied to derive new conclusions and those conclusions contradict with each other (e.g., from one we derive X and from the other we derive not X), we should go with the conclusion from the rule with higher preference. Based on the facts, rules, and preferences, what is the truth value of the statement,  does the butterfly reveal a secret to the fish? Answer 'proved' if it can be proved, 'disproved' if it can be disproved, and 'unknown' if it can neither be proved nor disproved.

---

## LOGIC-03: Causal Reasoning
**Domain:** Causal Reasoning
**Type:** exactMatch

Question: Sam throws a poisonous test tube towards Agent X, who, after seeing it, ducks. The test tube misses Agent X and he survives. Is Sam throwing the poisonous test tube a necessary cause for Agent X's survival? Reply based on the answer a logician would give.

---

## LOGIC-04: Decimal Number Comparison
**Domain:** Numerical Reasoning
**Type:** exactMatch

Which number is larger: 9.11 or 9.9? Give just the number.

---

## LOGIC-05: Pronoun Disambiguation
**Domain:** Natural Language Understanding / Coreference Resolution
**Type:** multipleChoice

Here is a sentence with pronoun(s) whose antecedent(s) can either be derived from the context or is ambiguous.
Sentence: The investigator wanted to interview the witness in person but he was too late. On his way, he got stuck in traffic.
Which of the following options correctly explains the antecedent(s) of the pronoun(s)?
(A) The witness got stuck in traffic.
(B) The investigator was too late.
(C) The witness got stuck in a meeting.
(D) The witness was too late.
(E) Ambiguous.

---

## LOGIC-06: Dyck Language Bracket Matching
**Domain:** Formal Language / Stack-Based Reasoning
**Type:** exactMatch

You are an expert in a language called dyck where you must complete the language sequence of unclosed brackets of all types (e.g., [], {}, <>). You are given an initial initial dyck language sequence and the steps, provided as
thoughts, that were used to arrive at the closing bracket sequence in the dyck language. Your job is to identify the first step that was a mistake in reasoning about the closing bracket sequence in dyck language, if any.
This can be forgetting to close a bracket or closing with the wrong bracket or incorrectly copying the prior subsequence of closing brackets to the next step.
Task: Complete the rest of the sequence, making sure that the parentheses are closed properly. Input: ( [ [ [ < { ( [ ( [ { [ ] } ] ) ] ) } > ( [ ( [ ] ( ) [ { [ ] } ] ) ] < ( ) > ) ] ] ] [ < > ] ( [ [ ] ] )
Thought 1: We should process each input one by one and keep track of the stack configuration.
Thought 2: stack: empty
Thought 3: ( ; stack: (
Thought 4: [ ; stack: ( [
Thought 5: [ ; stack: ( [ [
Thought 6: [ ; stack: ( [ [ [
Thought 7: < ; stack: ( [ [ [ <
Thought 8: { ; stack: ( [ [ [ < {
Thought 9: ( ; stack: ( [ [ [ < { (
Thought 10: [ ; stack: ( [ [ [ < { ( [
Thought 11: ( ; stack: ( [ [ [ < { ( [ (
Thought 12: [ ; stack: ( [ [ [ < { ( [ ( [
Thought 13: { ; stack: ( [ [ [ < { ( [ ( [ {
Thought 14: [ ; stack: ( [ [ [ < { ( [ ( [ { [
Thought 15: ] ; stack: ( [ [ [ < { ( [ ( [ {
Thought 16: } ; stack: ( [ [ [ < { ( [ ( [
Thought 17: ] ; stack: ( [ [ [ < { ( [ (
Thought 18: ) ; stack: ( [ [ [ < { ( [
Thought 19: ) ; stack: ( [ [ [ < {
Thought 20: } ; stack: ( [ [ [ <
Thought 21: > ; stack: ( [ [ [
Thought 22: ( ; stack: ( [ [ [ (
Thought 23: [ ; stack: ( [ [ [ ( [
Thought 24: [ ; stack: ( [ [ [ ( [ [
Thought 25: ] ; stack: ( [ [ [ ( [
Thought 26: ( ; stack: ( [ [ [ (
Thought 27: ) ; stack: ( [ [ [
Thought 28: ] ; stack: ( [ [
Thought 29: ] ; stack: ( [
Thought 30: ] ; stack: (
Thought 31: [ ; stack: [
Thought 32: < ; stack: [ <
Thought 33: > ; stack: [
Thought 34: ] ; stack: empty
Thought 35: ( ; stack: (
Thought 36: [ ; stack: ( [
Thought 37: [ ; stack: ( [ [
Thought 38: ] ; stack: ( [
Thought 39: ] ; stack: (
Thought 40: ) ; stack: empty
Thought 41: Now, we have reached the end. The final stack is empty.
Thought 42: So the answer is )
Q: Is there a mistake in this sequence? Write "No" if there are no mistakes, or the number N if there is a mistake in Thought N.

---

## LOGIC-07: Filtered List Sum
**Domain:** Constraint Satisfaction / Arithmetic
**Type:** exactMatch

Given the list [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], remove all elements that are strictly greater than 4. What is the sum of the remaining elements?

---

## LOGIC-08: SVG Path Shape Identification
**Domain:** Spatial Reasoning / Geometric Visualization
**Type:** multipleChoice

Suppose we draw this SVG path element: M -22.13862,-1.76669 L -21.88362,-1.32502 M -11.24144,28.41692 L -11.91099,29.53123 M -21.88362,-1.32502 L -21.11862,0.0 M 20.14782,6.99322 L 20.14782,8.18295 M 20.14782,2.09797 L 20.14782,6.99322 M -8.16043,37.85129 L -8.25499,38.00867 M -8.49703,27.73266 L -11.75207,33.14996 M -27.11862,11.40192 L -27.11862,10.20472 M -12.27151,30.13125 L -6.27134,33.73652 M -8.48969,0.0 L -14.14948,0.0 M -8.42356,38.28922 L -8.67547,38.70846 M -21.11862,7.86732 L -21.11862,11.40192 M -22.77222,-2.86412 L -22.13862,-1.76669 M -26.30862,-1.40296 L -24.11862,-5.19615 M 20.14782,8.68487 L 20.14782,8.85218 M -6.83352,34.56535 L -6.78638,34.59368 M -6.97496,34.48037 L -6.83352,34.56535 M 0.0,0.0 L 7.44663,0.0 M 13.68673,-7.38945 L 17.72892,-9.57183 M -11.75207,33.14996 L -12.61733,34.59 M -22.58922,11.40192 L -23.69862,11.40192 M 20.14782,8.18295 L 20.14782,8.68487 M -13.62151,7.35424 L -10.55931,5.70096 M 0.0,8.85218 L 0.0,2.036 L 0.0,1.6288 M -6.26766,27.90557 L -6.60978,26.53336 M -21.11862,11.40192 L -22.58922,11.40192 M -23.63392,-4.35662 L -22.77222,-2.86412 M -11.59094,38.70661 L -9.3069,39.21569 M 10.63735,-5.7431 L 13.68673,-7.38945 M -27.11862,0.0 L -26.30862,-1.40296 M -15.1959,8.20425 L -13.62151,7.35424 M -14.14948,0.0 L -17.07652,0.0 M 9.67095,0.0 L 20.14782,-0.0 M 0.0,0.0 L -8.48969,0.0 M -7.64355,34.07865 L -6.97496,34.48037 M -6.77742,25.86098 L -6.95191,25.16116 M -27.11862,10.20472 L -27.11862,5.70096 M -21.11862,0.0 L -21.11862,7.86732 M -9.26995,29.60151 L -6.9556,30.99211 M 20.14782,8.85218 L 17.42787,8.85218 M -24.99822,11.40192 L -27.11862,11.40192 M -6.26766,27.90557 L -12.35879,32.52875 M -8.25499,38.00867 L -8.29949,38.08273 M -11.24144,28.41692 L -9.26995,29.60151 M 17.42787,8.85218 L 13.10314,8.85218 M 0.0,0.0 L 10.63735,-5.7431 M -9.3069,39.21569 L -8.5044,39.39456 M -17.07652,0.0 L -21.11862,0.0 M -24.11862,-5.19615 L -23.63392,-4.35662 M 9.268,8.85218 L 0.0,8.85218 M -6.64498,26.39216 L -6.77742,25.86098 M -8.29949,38.08273 L -8.42356,38.28922 M -21.11862,11.40192 L -15.1959,8.20425 M 20.14782,-0.0 L 20.14782,2.09797 M 13.10314,8.85218 L 9.268,8.85218 M 7.44663,0.0 L 9.67095,0.0 M -12.35879,32.52875 L -14.84671,34.41709 M -23.69862,11.40192 L -24.99822,11.40192 M -6.60978,26.53336 L -6.64498,26.39216 M -27.11862,5.70096 L -27.11862,0.0 M 0.0,1.6288 L 0.0,0.0 M -10.55931,5.70096 L 0.0,0.0 . Out of the following shapes:
1. rectangle that is not a square and with no diagonals drawn
2. square with no diagonals drawn
3. triangle that is not a right triangle
4. right triangle
5. parallelogram that is not a rectangle and with no diagonals drawn
6. trapezoid with exactly one pair of parallel sides and with no diagonals drawn
7. irregular convex pentagon with no diagonals drawn
8. irregular concave pentagon with no diagonals drawn
9. regular pentagon with no diagonals drawn
10. regular hexagon with no diagonals drawn
which one(s) can be viewed when the lines in the SVG are visualized? Note that a shape with n sides should not necessarily be drawn by n lines; e.g., a triangle might be drawn by 4 lines, two of which collinear.
Options:
(A) 1, 4 and 10
(B) 1, 7 and 5
(C) 1, 4, 3 and 10
(D) only 7
(E) 1, 4, 7 and 8
(F) 1, 4, 7, 5 and 6
(G) 7, 8 and 10
(H) 1, 4 and 7
(I) 1 and 7
(J) 4 and 7
(K) 4, 7 and 8
(L) only 4
(M) none of the above
(N) 1, 7 and 3
(O) 4, 7 and 9
(P) 1 and 4
Coordinates have been rounded to 5 decimal places so ignore slight differences.

---

## LOGIC-09: Adjective Order in Variant English
**Domain:** Natural Language / Constraint Satisfaction
**Type:** exactMatch

In a variant of English, we are given that the following sentences have correct adjective order:
(1) brand-new umbrella (2) huge car key (3) drinking flower pot (4) blue fire extinguisher (5) ethiopian jar (6) brown table (7) brown drinking sunglasses (8) old-fashioned car (9) obnoxious scissors (10) silly indonesian plate (11) typing necklace (12) hiking trash can (13) awful brazilian camera (14) new rectangular clock (15) bangladeshi key (16) plastic bicycle (17) exercise enormous filipino car (18) large knife (19) old triangular drill (20) mexican fork (21) new fork (22) blue whittling wrench (23) silly shoe (24) enormous sofa (25) normal-size hammer (26) new rectangular book (27) exercise knife (28) crimson plastic ridiculous piano (29) magenta bag (30) new guitar (31) green umbrella (32) prismlike guitar (33) good knife (34) indigo eating fork (35) square pen (36) terrible bottle (37) blue scissors (38) snorkeling scissors (39) crimson snorkeling hammer (40) cardboard chair (41) walking lamp (42) old-fashioned rectangular scissors (43) driving bowl (44) exercise scissors (45) ancient fork (46) obnoxious chair (47) big earring (48) tiny steel banana (49) wonderful congolese dog (50) spherical table (51) massive wool earring (52) pyramidal pen (53) old car

In this variant of English, which of the following sentences (Options A-J) use the correct adjective order? If none of the sentences (Options A-J) use the correct adjective order, select option K. Select all that apply.
(A) prismlike brand-new normal-size wool good vietnamese hiking violet ring
(B) walking tiny cloth lovely japanese pyramidal new plate
(C) walking midsize leather repulsive pakistani archaic spherical dog
(D) green hiking huge plastic terrible american new square toolbox
(E) normal-size leather repulsive egyptian pyramidal brand-new shoe
(F) circular medium-size cardboard obnoxious iranian typing yellow ball
(G) brand-new triangular huge glass obnoxious vietnamese dog
(H) aqua driving normal-size steel obnoxious pakistani saw
(I) old-fashioned square large steel lovely turkish whittling knife
(J) rectangular new massive paper silly american snorkeling saw
(K) None of the above

Provide your final answer as a concatenation of all the correct choices. For example, if B and C have correct adjective order, then your final answer must be "BC".

---

## LOGIC-10: Object Counting with Distractors
**Domain:** Counting / Information Extraction
**Type:** exactMatch

My friend has 80 pineapples. I have 19 nissan ariya cars (it is a funny story how I have 19 of them: initially I had 89, then I also got another 18 making it a total of 107, then I got another 99 making it a total of 206, but then I lost 187 of them so eventually I am left with 19 of them now). I also have 54 muscat grapes (very happy to have them). My mother has 23 honda cr-v cars. I also have 1 samsung galaxy a55 mobiles (it is a funny story how I have 1 of them: initially I had 49, then I also got another 62 making it a total of 111, then I got another 17 making it a total of 128, but then I lost 127 of them so eventually I am left with 1 of them now). I also have 5 toyota prius cars (it is a funny story how I have 5 of them: initially I had 62, then I also got another 69 making it a total of 131, then I got another 66 making it a total of 197, but then I lost 192 of them so eventually I am left with 5 of them now). I also have 24 nebbiolo grapes (here is why I have these many: initially I had 29 of them, then I lost 28 of them, but then I got another 26 of them, but then I lost 3 of them, so at the end I am left with 24 of them). I also have 45 zte mobiles (received them yesterday). I also have 60 vivo mobiles (here is why I have these many: initially I had 75 of them, then I lost 18 of them, but then I got another 28 of them, but then I lost 25 of them, so at the end I am left with 60 of them). My father has 86 elderberryoranges. My aunt has 50 samsung galaxy a16 mobiles. I also have 43 mazda cx-5 cars (here is why I have these many: initially I had 24 of them, then I lost 17 of them, but then I got another 50 of them, but then I lost 14 of them, so at the end I am left with 43 of them). My sister has 35 nissan pathfinder cars. My brother has 43 mazda6 cars. I also have 84 iphone 15 mobiles (received them last week). My grandmother has 40 raspberrys. My mother also has 61 jeep gladiator cars. I also have 89 durians (it is a funny story how I have 89 of them: initially I had 18, then I also got another 96 making it a total of 114, then I got another 56 making it a total of 170, but then I lost 81 of them so eventually I am left with 89 of them now). My cousin has 93 honeycrisp apples. I also have 5 watermelons (I am in love with them). My cousin also has 48 buick enclave cars. I also have 62 ginger gold apples (it is a funny story how I have 62 of them: initially I had 64, then I also got another 21 making it a total of 85, then I got another 69 making it a total of 154, but then I lost 92 of them so eventually I am left with 62 of them now). My grandfather has 51 honda insight cars. My uncle has 5 samsung galaxy c55 mobiles. My uncle also has 15 google (pixel) mobiles. I also have 25 jazz apples (I really like them). I also have 50 iphone 11 mobiles (here is why I have these many: initially I had 83 of them, then I lost 66 of them, but then I got another 97 of them, but then I lost 64 of them, so at the end I am left with 50 of them). My cousin also has 99 blackberry mobiles. My sister also has 74 samsung galaxy s24 mobiles. My father also has 37 jonagold apples. My mother also has 27 toyota avalon cars. My friend also has 10 mazda cx-80 cars. My grandfather also has 63 honeydews. My father also has 86 htc mobiles. My father also has 60 lg mobiles. I also have 39 fuji apples (feeling great about this). My friend also has 97 tecno mobiles. My cousin also has 57 samsung galaxy a35 mobiles. My friend also has 94 kia niro cars. My friend also has 63 subaru impreza cars. I also have 92 persimmons (here is why I have these many: initially I had 56 of them, then I lost 16 of them, but then I got another 82 of them, but then I lost 30 of them, so at the end I am left with 92 of them). I also have 37 honda odyssey cars (it is a funny story how I have 37 of them: initially I had 24, then I also got another 78 making it a total of 102, then I got another 38 making it a total of 140, but then I lost 103 of them so eventually I am left with 37 of them now). My aunt also has 4 iphone 8 mobiles. I also have 7 gala apples (maybe I just need some of them). My sister also has 45 iphone 13 mobiles. I also have 62 nissan sentra cars (it is a funny story how I have 62 of them: initially I had 77, then I also got another 50 making it a total of 127, then I got another 88 making it a total of 215, but then I lost 153 of them so eventually I am left with 62 of them now). I also have 8 dodge challenger cars (it is a funny story how I have 8 of them: initially I had 14, then I also got another 95 making it a total of 109, then I got another 29 making it a total of 138, but then I lost 130 of them so eventually I am left with 8 of them now). My grandfather also has 28 coconuts. My friend also has 49 toyota tacoma cars. My father also has 93 grapefruits. My uncle also has 19 mazda cx-50 cars. My mother also has 27 toyota highlander cars. I also have 39 nissan leaf cars (it is a funny story how I have 39 of them: initially I had 93, then I also got another 57 making it a total of 150, then I got another 100 making it a total of 250, but then I lost 211 of them so eventually I am left with 39 of them now). I also have 46 mazda cx-30 cars (one day, I will have more of them). My mother also has 27 toyota corolla cars. My brother also has 76 toyota tundra cars. My mother also has 10 huawei pura 70 mobiles. My uncle also has 25 peaches. I also have 9 huawei nova 12 pro mobiles (it is a funny story how I have 9 of them: initially I had 65, then I also got another 70 making it a total of 135, then I got another 78 making it a total of 213, but then I lost 204 of them so eventually I am left with 9 of them now). My brother also has 1 ford edge cars. My mother also has 73 lychees. I also have 92 toyota 4runnertoyota sequoia cars (it is a funny story how I have 92 of them: initially I had 89, then I also got another 69 making it a total of 158, then I got another 28 making it a total of 186, but then I lost 94 of them so eventually I am left with 92 of them now). I also have 67 honor mobiles (I like these a lot). I also have 29 pink lady apples (planning to have more in the future). I also have 15 huawei mate x6 mobiles (here is why I have these many: initially I had 88 of them, then I lost 33 of them, but then I got another 87 of them, but then I lost 127 of them, so at the end I am left with 15 of them). I also have 9 starfruits (here is why I have these many: initially I had 68 of them, then I lost 56 of them, but then I got another 44 of them, but then I lost 47 of them, so at the end I am left with 9 of them). I also have 30 huawei pura 70 pro mobiles (it is a funny story how I have 30 of them: initially I had 89, then I also got another 72 making it a total of 161, then I got another 92 making it a total of 253, but then I lost 223 of them so eventually I am left with 30 of them now). I also have 53 mazda cx-70 cars (here is why I have these many: initially I had 53 of them, then I lost 26 of them, but then I got another 29 of them, but then I lost 3 of them, so at the end I am left with 53 of them). My sister also has 6 honda accord cars. My mother also has 83 iphone 4 mobiles. I also have 66 subaru ascent cars (here is why I have these many: initially I had 41 of them, then I lost 16 of them, but then I got another 79 of them, but then I lost 38 of them, so at the end I am left with 66 of them). My uncle also has 39 plums. I also have 90 nissan rogue cars (it is a funny story how I have 90 of them: initially I had 48, then I also got another 34 making it a total of 82, then I got another 10 making it a total of 92, but then I lost 2 of them so eventually I am left with 90 of them now). My aunt also has 72 honda passport cars. My father also has 41 nissan armada cars. My cousin also has 23 iphone 14 mobiles. My grandfather also has 50 samsung galaxy tab s10 mobiles. I also have 59 grenache grapes (here is why I have these many: initially I had 82 of them, then I lost 50 of them, but then I got another 57 of them, but then I lost 30 of them, so at the end I am left with 59 of them). I also have 17 huawei nova 12s mobiles (received them yesterday). My aunt also has 24 honda civic cars. My mother also has 45 mazda cx-3 cars. I also have 20 iphone 16 mobiles (hope to have more in the future). I also have 96 audi a6 cars (they are great). I also have 65 nissan altima cars (here is why I have these many: initially I had 18 of them, then I lost 16 of them, but then I got another 86 of them, but then I lost 23 of them, so at the end I am left with 65 of them). My brother also has 43 nissan murano cars. My father also has 91 dates. My father also has 70 ambrosia apples. My brother also has 4 plantains. I also have 30 kiwis (it is a funny story how I have 30 of them: initially I had 76, then I also got another 29 making it a total of 105, then I got another 35 making it a total of 140, but then I lost 110 of them so eventually I am left with 30 of them now). My grandmother also has 56 iphone 6 mobiles. My grandmother also has 16 honda pilot cars. I also have 31 cranberrys (here is why I have these many: initially I had 46 of them, then I lost 11 of them, but then I got another 25 of them, but then I lost 29 of them, so at the end I am left with 31 of them). My sister also has 90 oppo mobiles. My sister also has 11 mulberrys. My mother also has 9 realme mobiles. My aunt also has 7 meizu mobiles. I also have 78 pomegranates (it is a funny story how I have 78 of them: initially I had 45, then I also got another 45 making it a total of 90, then I got another 60 making it a total of 150, but then I lost 72 of them so eventually I am left with 78 of them now). I also have 39 sony mobiles (maybe I just need some of them). My cousin also has 28 samsung galaxy z fold5 mobiles. I also have 11 nissan titan cars (it is a funny story how I have 11 of them: initially I had 44, then I also got another 61 making it a total of 105, then I got another 69 making it a total of 174, but then I lost 163 of them so eventually I am left with 11 of them now). I also have 15 infinix mobiles (I do not think I need this much).  What is the absolute difference of the total number of mobiles and fruits that I have?

---

## LOGIC-11: Object Property Tracking
**Domain:** State Tracking / Constraint Satisfaction
**Type:** exactMatch

I had a collection of 45 weird items that went through a few changes. Initially, I had a medium Portuguese ball made of steel with a smell of gasoline, a medium Italian brush made of concrete with a smell of coconut, a medium Portuguese plier made of steel with a smell of coffee, an extra-small Japanese brush made of plastic with a smell of pine needles, an extra-large Turkish book made of steel with a smell of vinegar, a large Turkish bottle made of steel with a smell of gasoline, an extra-large British dog made of steel with a smell of rose, a large Afghan hammer made of steel with a smell of leather, a small Mexican pen made of plastic with a smell of pine needles, an extra-extra-small Polish drill made of ceramic with a smell of freshly cut grass, a small Canadian screwdriver made of glass with a smell of coconut, an extra-small Afghan stapler made of steel with a smell of burning wood, an extra-extra-small Russian plier made of ceramic with a smell of coconut, a medium Chinese shoe made of plastic with a smell of freshly cut grass, an extra-extra-small Japanese sofa made of steel with a smell of baking bread, a small Mexican hat made of steel with a smell of citrus fruits, a large French key made of glass with a smell of garlic, an extra-small Mexican cup made of glass with a smell of garlic, a small Portuguese shirt made of ceramic with a smell of gasoline, an extra-extra-large Iranian fork made of plastic with a smell of citrus fruits, a small Spanish cup made of concrete with a smell of leather, a large Spanish car made of concrete with a smell of popcorn, an extra-large Chinese table made of concrete with a smell of gasoline, a medium Canadian pen made of ceramic with a smell of pine needles, an extra-small Mexican ball made of steel with a smell of popcorn, an extra-extra-large Mexican bed made of ceramic with a smell of rose, an extra-large Spanish screwdriver made of concrete with a smell of garlic, a large Russian sunglasses made of concrete with a smell of coffee, an extra-small Polish house made of glass with a smell of burning wood, an extra-extra-small Japanese brush made of glass with a smell of garlic, an extra-small Brazilian fork made of concrete with a smell of citrus fruits, an extra-extra-large Russian canvas made of plastic with a smell of leather, a small Iranian calculator made of glass with a smell of coffee, an extra-small Brazilian lamp made of ceramic with a smell of lavender, a medium Canadian apple made of steel with a smell of coconut, a medium Afghan hat made of concrete with a smell of popcorn, a large Iranian piano made of ceramic with a smell of gasoline, a medium Russian saw made of steel with a smell of lavender, an extra-extra-large Turkish trash can made of glass with a smell of citrus fruits, a large Canadian plier made of steel with a smell of baking bread, an extra-large Chinese pencil made of plastic with a smell of garlic, a small Chinese wallet made of concrete with a smell of vanilla, an extra-small Portuguese banana made of concrete with a smell of chocolate, a medium French screwdriver made of concrete with a smell of freshly cut grass, an extra-extra-small German saw made of glass with a smell of baking bread. The color of the items was respectively as follows: the first 4 were beige, the next 1 was black, the next 4 were brown, the next 3 were crimson, the next 1 was cyan, the next 3 were gold, the next 1 was gray, the next 1 was green, the next 7 were indigo, the next 1 was ivory, the next 2 were orange, the next 1 was pink, the next 3 were purple, the next 1 was red, the next 3 were silver, the next 3 were turquoise, the next 2 were violet, the next 4 were yellow. Then, my friend took any item with a smell of lavender, garlic or gasoline in my collection and threw it away. Then, for each item of size extra-small in my new collection, my aunt took it but then gave me another one of the same item made of her favorite material and with a smell of vanilla (all other properties the same). After this, my new collection had: 13 item(s) made of concrete, 8 item(s) made of steel, 4 item(s) made of plastic, 4 item(s) made of ceramic, 4 item(s) made of glass. Then my dad threw away all item of a certain color from my new collection. After this, my new collection only had: 3 beige item(s), 3 brown item(s), 3 crimson item(s), 1 cyan item(s), 3 gold item(s), 5 indigo item(s), 1 ivory item(s), 1 orange item(s), 1 pink item(s), 2 purple item(s), 1 red item(s), 2 silver item(s), 1 turquoise item(s), 1 violet item(s), 4 yellow item(s). Then, for any item of color purple in my new collection, my mom gave me another one of the same item, but with a orange color, Japanese origin, small size, freshly cut grass smell, and made of plastic. Then, my fiance compared my new collection with my initial collection and if there was an item in my new collection with a (smell, color) pair that was different from the (smell, color) pair of all items in my initial collection, she added another copy of that to my new collection.  Then, I lost one of the extra-extra-large items in my collection.  In my current collection, how many items have the following attributes: color is not orange, size is not extra-extra-large, material is not steel, smell is not popcorn, and origin is not Iranian? If the exact number cannot be computed, the answer must be "unknown".

---

## LOGIC-12: Linear Ordering from Comparisons
**Domain:** Ordering / Transitive Reasoning
**Type:** exactMatch

Alice is taller than Bob. Charlie is shorter than Diana. Diana is shorter than Bob. Eve is taller than Alice. Rank all five people from shortest to tallest, separated by commas.

---

## LOGIC-13: River Crossing Puzzle
**Domain:** Constraint Satisfaction / Planning
**Type:** exactMatch

A farmer needs to cross a river with a wolf, a goat, and a cabbage. The boat can carry the farmer and up to TWO other items at the same time. The wolf will eat the goat if left alone together without the farmer, and the goat will eat the cabbage if left alone together without the farmer. What is the minimum number of trips across the river the farmer needs to make to get everything safely to the other side?

---

## LOGIC-14: Sarcasm Detection
**Domain:** Natural Language Understanding / Pragmatics
**Type:** exactMatch

Here are three (post, reply) pairs from Reddit. Your task is to decide whether each reply is sarcastic. Specifically, label each pair with a "0" or "1", wherea "1" indicates that the reply is sarcastic, and a "0" indicates that the reply does not contain sarcasm, and provide your final answer as a comma-separated set of labels (e.g., "1,0,0" or "0,0,0").

POST 1: We should dig up all the confederate soldiers and cremate them, so we can erase these racists from the books!
REPLY 1: I'm sure people are less concerned with having a picnic around a confederate general than *hey lets dig up some dead people*

POST 2: OMG, it's videos like these of Alex definitely pretending to have a good time, while trying to fight through the pain of bullying that are part of the problem!
REPLY 2: KILLER KIDWELL ROLLS WITH JOHN ROCKER,,YOU BIG BROTHER TERDMUFFINS CAN BUZZ OFF BZZZZ BZZZZ BZZZZZZZZ

POST 3: Older Redditors: what do you remember doing routinely, or maybe still do, that younger Redditors have probably never done?
REPLY 3: - Getting home and checking the answering machine - Walking to anything within 3 miles - Having someone clean my windshield with brown paper towels - Whipping a disobedient slave

---

## LOGIC-15: Shuffled Object Tracking
**Domain:** State Tracking / Sequential Reasoning
**Type:** multipleChoice

Alice, Bob, Claire, Dave, Eve, Fred, and Gertrude are friends and avid readers who occasionally trade books. At the start of the semester, they each buy one new book: Alice gets The Fellowship of the Ring, Bob gets Ulysses, Claire gets The Pearl, Dave gets The Great Gatsby, Eve gets Frankenstein, Fred gets The Odyssey, and Gertrude gets Moby Dick.
As the semester proceeds, they start trading around the new books. First, Claire and Dave swap books. Then, Gertrude and Dave swap books (let's call it Action 1). Then, Dave and Claire swap books (let's call it Action 2). Then, Claire and Dave swap books (let's call it Action 3). Then, Dave and Gertrude swap books (let's call it Action 4). Then, Alice and Fred swap books (let's call it Action 5). Then, Alice and Fred discuss something (let's call it Action 6). Then, Alice and Fred swap books. Then, Fred and Alice swap books (let's call it Action 7). Then, Alice and Fred swap books. Then, Dave and Fred swap books (let's call it Action 8). Then, Fred and Eve swap books (let's call it Action 9). Then, Eve and Fred swap books (let's call it Action 10). Then, Fred and Dave swap books (let's call it Action 11). Then, nothing happens for a while (let's call it Action 12). Then, nothing happens for a while. Then, Fred and Bob swap books (let's call it Action 13). Then, Bob and Fred swap books (let's call it Action 14). Then, Claire and Alice swap books (let's call it Action 15). Then, Claire and Alice discuss something (let's call it Action 16). Then, Claire and Alice swap books. Then, Dave and Gertrude swap books. Then, Gertrude and Eve swap books (let's call it Action 17). Then, Eve and Gertrude swap books (let's call it Action 18). Then, Gertrude and Dave swap books. Then, Alice and Gertrude swap books (let's call it Action 19). Then, Gertrude and Bob swap books (let's call it Action 20). Then, Bob and Gertrude swap books (let's call it Action 21). Then, Gertrude and Alice swap books (let's call it Action 22). Then, Alice and Fred swap books. Then, Fred and Claire swap books (let's call it Action 23). Then, Claire and Fred swap books (let's call it Action 24). Then, Fred and Alice swap books. Then, Action 21 repeats. Then, Action 20 repeats. Then, nothing happens for a while. Then, Fred and Bob swap books. Then, Fred and Bob discuss something (let's call it Action 25). Then, Fred and Bob swap books. Then, Eve and Fred swap books. Then, Fred and Eve swap books. Then, Bob and Gertrude swap books. Then, Gertrude and Bob swap books. Then, Claire and Eve swap books (let's call it Action 26). Then, Eve and Claire swap books (let's call it Action 27). Then, nothing happens for a while. Then, Eve and Alice swap books (let's call it Action 28). Then, Alice and Fred swap books. Then, Fred and Alice swap books. Then, Alice and Eve swap books (let's call it Action 29). Then, Fred and Alice swap books. Then, Fred and Alice discuss something (let's call it Action 30). Then, Fred and Alice swap books. Then, Gertrude and Eve swap books. Then, Eve and Bob swap books (let's call it Action 31). Then, Bob and Eve swap books (let's call it Action 32). Then, Eve and Gertrude swap books. Then, Gertrude and Alice swap books. Then, Action 19 repeats. Then, nothing happens for a while. Then, Alice and Bob swap books (let's call it Action 33). Then, Bob and Alice swap books (let's call it Action 34). Then, Action 2 repeats. Then, Claire and Gertrude swap books (let's call it Action 35). Then, Gertrude and Claire swap books (let's call it Action 36). Then, Claire and Dave swap books. Then, Alice and Claire swap books (let's call it Action 37). Then, Alice and Claire discuss something (let's call it Action 38). Then, Alice and Claire swap books. Then, nothing happens for a while. Then, nothing happens for a while. Then, Action 29 repeats. Then, Alice and Eve discuss something (let's call it Action 39). Then, Alice and Eve swap books. Then, Fred and Dave swap books. Then, Dave and Bob swap books (let's call it Action 40). Then, Bob and Dave swap books (let's call it Action 41). Then, Action 8 repeats. Then, Action 12 repeats. Then, Alice and Eve swap books. Then, Eve and Bob swap books. Then, Eve and Bob discuss something (let's call it Action 42). Then, Eve and Bob swap books. Then, nothing happens for a while. Then, Fred and Alice swap books. Then, Alice and Dave swap books (let's call it Action 43). Then, Dave and Alice swap books (let's call it Action 44). Then, Action 5 repeats. Then, Eve and Alice swap books. Then, Action 29 repeats. Then, Action 12 repeats. Then, Gertrude and Dave swap books. Then, Gertrude and Dave discuss something (let's call it Action 45). Then, Gertrude and Dave swap books. Then, Eve and Dave swap books (let's call it Action 46). Then, Action 40 repeats. Then, Action 41 repeats. Then, Dave and Eve swap books (let's call it Action 47). Then, Eve and Gertrude swap books. Then, Eve and Gertrude discuss something (let's call it Action 48). Then, Eve and Gertrude swap books. Then, Alice and Gertrude swap books. Then, Action 22 repeats. Then, nothing happens for a while. Then, Claire and Dave swap books. Then, Claire and Dave discuss something (let's call it Action 49). Then, Claire and Dave swap books. Then, Claire and Dave swap books. Then, Action 2 repeats. Then, nothing happens for a while. Then, Action 41 repeats. Then, Dave and Fred swap books. Then, Fred and Dave swap books. Then, Action 40 repeats. Then, Claire and Eve swap books. Then, Claire and Eve discuss something (let's call it Action 50). Then, Action 26 repeats. Then, Dave and Fred swap books. Then, Dave and Fred discuss something (let's call it Action 51). Then, Dave and Fred swap books. Then, Eve and Fred swap books. Then, Action 11 repeats. Then, Dave and Fred swap books. Then, Fred and Eve swap books. Then, Alice and Bob swap books. Then, Bob and Claire swap books (let's call it Action 52). Then, Claire and Bob swap books (let's call it Action 53). Then, Bob and Alice swap books. Then, Dave and Alice swap books. Then, Alice and Dave swap books. Then, Alice and Bob swap books. Then, Bob and Claire swap books. Then, Claire and Bob swap books. Then, Bob and Alice swap books. Then, nothing happens for a while. Then, Gertrude and Fred swap books (let's call it Action 54). Then, Fred and Gertrude swap books (let's call it Action 55). Then, Bob and Dave swap books. Then, Dave and Bob swap books. Then, Claire and Alice swap books. Then, Alice and Fred swap books. Then, Action 7 repeats. Then, Action 37 repeats. Then, nothing happens for a while. Then, Dave and Alice swap books. Then, Dave and Alice discuss something (let's call it Action 56). Then, Dave and Alice swap books. Then, Action 29 repeats. Then, Eve and Bob swap books. Then, Bob and Eve swap books. Then, Eve and Alice swap books. Then, Dave and Claire swap books. Then, Dave and Claire discuss something (let's call it Action 57). Then, Dave and Claire swap books. Then, Action 35 repeats. Then, Action 17 repeats. Then, Action 18 repeats. Then, Gertrude and Claire swap books. Then, Bob and Fred swap books. Then, Bob and Fred discuss something (let's call it Action 58). Then, Action 14 repeats. Then, Alice and Fred swap books. Then, Fred and Alice swap books. Then, Fred and Eve swap books. Then, Action 10 repeats. Then, Gertrude and Alice swap books. Then, Gertrude and Alice discuss something (let's call it Action 59). Then, Gertrude and Alice swap books. Then, Dave and Claire swap books. Then, Action 35 repeats. Then, Gertrude and Claire swap books. Then, Claire and Dave swap books. Then, Action 10 repeats. Then, Action 9 repeats. Then, Action 12 repeats. Then, nothing happens for a while. Then, Action 54 repeats. Then, Fred and Gertrude swap books. Then, Gertrude and Dave swap books. Then, Bob and Eve swap books. Then, Eve and Bob swap books. Then, Action 41 repeats. Then, Dave and Eve swap books. Then, Eve and Dave swap books. Then, Dave and Bob swap books. Then, nothing happens for a while. Then, Eve and Dave swap books. Then, Dave and Bob swap books. Then, Action 41 repeats. Then, Dave and Eve swap books. Then, Bob and Dave swap books. Then, Dave and Alice swap books. Then, Action 43 repeats. Then, Action 40 repeats. Then, Alice and Fred swap books. Then, Action 9 repeats. Then, Eve and Fred swap books. Then, Action 7 repeats. Then, Dave and Eve swap books. Then, Dave and Eve discuss something (let's call it Action 60). Then, Dave and Eve swap books. Then, Alice and Eve swap books. Then, Action 28 repeats. Then, Action 8 repeats. Then, Fred and Gertrude swap books. Then, Gertrude and Fred swap books. Then, Fred and Dave swap books. Then, Action 27 repeats. Then, Claire and Bob swap books. Then, Bob and Claire swap books. Then, Claire and Eve swap books. Then, Action 12 repeats. Then, nothing happens for a while. Then, Gertrude and Dave swap books. Then, Action 45 repeats. Then, Gertrude and Dave swap books. Then, Dave and Claire swap books. Then, Action 57 repeats. Then, Dave and Claire swap books. Then, Action 8 repeats. Then, Action 51 repeats. Then, Dave and Fred swap books. Then, Dave and Gertrude swap books. Then, Dave and Gertrude discuss something (let's call it Action 61). Then, Dave and Gertrude swap books. Then, Fred and Claire swap books. Then, Fred and Claire discuss something (let's call it Action 62). Then, Fred and Claire swap books. Then, Claire and Fred swap books. Then, Fred and Eve swap books. Then, Action 10 repeats. Then, Fred and Claire swap books. Then, Dave and Eve swap books. Then, Eve and Dave swap books. Then, Action 9 repeats. Then, Fred and Eve discuss something (let's call it Action 63). Then, Fred and Eve swap books. Then, Action 46 repeats. Then, Dave and Eve swap books. Then, Action 12 repeats. Then, Claire and Fred swap books. Then, Claire and Fred discuss something (let's call it Action 64). Then, Action 24 repeats. Then, Eve and Gertrude swap books. Then, Gertrude and Alice swap books. Then, Alice and Gertrude swap books. Then, Action 17 repeats. Then, Dave and Fred swap books. Then, Dave and Fred discuss something. Then, Dave and Fred swap books. Then, Bob and Dave swap books. Then, Dave and Bob swap books. Then, Action 12 repeats. Then, nothing happens for a while. Then, Action 33 repeats. Then, Bob and Alice swap books. Then, nothing happens for a while. Then, Claire and Dave swap books. Then, Action 2 repeats. Then, Action 12 repeats. Then, Fred and Bob swap books. Then, Action 14 repeats. Then, Bob and Dave swap books. Then, Action 40 repeats. Then, Action 2 repeats. Then, Action 3 repeats. Then, Gertrude and Eve swap books. Then, Gertrude and Eve discuss something (let's call it Action 65). Then, Gertrude and Eve swap books. Then, nothing happens for a while. Then, Gertrude and Alice swap books. Then, Alice and Gertrude swap books. Then, Action 17 repeats. Then, Eve and Dave swap books. Then, Dave and Eve swap books. Then, Eve and Gertrude swap books. Then, nothing happens for a while. Then, Claire and Dave swap books. Then, Claire and Dave discuss something. Then, Claire and Dave swap books. Then, Alice and Claire swap books. Then, Alice and Claire discuss something. Then, Alice and Claire swap books. Then, Alice and Fred swap books. Then, Action 15 repeats. Then, Claire and Alice discuss something. Then, Action 15 repeats. Then, Bob and Fred swap books. Then, Fred and Dave swap books. Then, Dave and Fred swap books. Then, Fred and Bob swap books. Then, Action 52 repeats. Then, Bob and Claire discuss something (let's call it Action 66). Then, Action 52 repeats. Then, Dave and Gertrude swap books. Then, Dave and Gertrude discuss something. Then, Dave and Gertrude swap books. Then, Dave and Alice swap books. Then, Action 37 repeats. Then, Action 15 repeats. Then, Alice and Dave swap books. Then, Bob and Alice swap books. Then, Alice and Bob swap books. Then, Claire and Alice swap books. Then, Alice and Claire swap books. Then, Gertrude and Bob swap books. Then, Bob and Gertrude swap books. Then, Action 31 repeats. Then, Bob and Eve swap books. Then, Bob and Alice swap books. Then, Alice and Gertrude swap books. Then, Gertrude and Alice swap books. Then, Alice and Bob swap books. Then, nothing happens for a while. Then, Alice and Claire swap books. Then, Claire and Alice swap books. Then, nothing happens for a while. Then, Gertrude and Alice swap books. Then, Gertrude and Alice discuss something. Then, Gertrude and Alice swap books. Then, Bob and Fred swap books. Then, Fred and Bob swap books. Then, Fred and Alice swap books. Then, Alice and Fred swap books. Then, Gertrude and Bob swap books. Then, Gertrude and Bob discuss something (let's call it Action 67). Then, Action 20 repeats. Then, Fred and Bob swap books. Then, Bob and Gertrude swap books. Then, Gertrude and Bob swap books. Then, Bob and Fred swap books. Then, Action 34 repeats. Then, Action 33 repeats. Then, Gertrude and Eve swap books. Then, Eve and Bob swap books. Then, Bob and Eve swap books. Then, Eve and Gertrude swap books. Then, Fred and Dave swap books. Then, Action 8 repeats. Then, Action 12 repeats. Then, Bob and Claire swap books. Then, Alice and Eve swap books. Finally, Eve and Claire swap books. At the end of the semester, Fred has
Options:
(A) The Fellowship of the Ring
(B) Ulysses
(C) The Pearl
(D) The Great Gatsby
(E) Frankenstein
(F) The Odyssey
(G) Moby Dick

---

## LOGIC-16: Spatial Rotation
**Domain:** Spatial Reasoning
**Type:** exactMatch

A cube has its faces painted different colors: top is red, bottom is blue, front is green, back is yellow, left is white, right is orange. I rotate the cube 90 degrees toward me (the top face tilts toward me, the front face goes down). After this single rotation, what color is on top?

---

## LOGIC-17: Temporal Scheduling
**Domain:** Temporal Reasoning / Constraint Satisfaction
**Type:** exactMatch

Rachel, Isabella and Lisa work from 9 to 5 their local time on weekdays. They want to have a meeting some time this week.

The schedule for Rachel's week in their local time is as follows:
Monday: Free only at the following times: from 9:00 to 9:20, from 10:35 to 11:30, from 12:15 to 17:00
Tuesday: Booked at the following times: from 9:35 to 11:00, from 11:15 to 12:35
Wednesday: Booked at the following times: from 10:15 to 11:20, from 11:55 to 12:55, from 13:55 to 14:45
Thursday: Booked at the following times: from 9:50 to 10:30, from 11:00 to 11:10
Friday: Free only at the following times: anytime before 9:25, from 10:45 to 11:10, from 12:00 to 13:20, from 14:40 to 15:15, anytime after 15:30


The schedule for Isabella's week in their local time is as follows:
Monday: Booked at the following times: anytime before 10:05, from 10:05 to 10:20, from 10:30 to 11:40, from 12:05 to 13:15
Tuesday: Booked at the following times: from 10:15 to 11:35, from 11:40 to 12:30, from 12:45 to 13:10, from 14:15 to 14:40
Wednesday: Booked at the following times: from 9:05 to 10:35, from 11:40 to 12:30, from 13:25 to 14:40, from 16:10 to 16:50
Thursday: Booked at the following times: from 9:50 to 11:20, from 12:50 to 13:30, from 13:50 to 14:50, from 15:20 to 15:40
Friday: Booked at the following times: from 10:00 to 11:25, from 11:25 to 11:40


The schedule for Lisa's week in their local time is as follows:
Monday: Booked at the following times: from 9:40 to 9:55, from 11:05 to 12:20, from 13:45 to 15:15, from 15:25 to 16:10
Tuesday: Booked at the following times: from 9:10 to 10:00, from 11:30 to 11:55, from 12:20 to 12:35
Wednesday: Booked at the following times: from 10:20 to 10:35, from 12:05 to 12:35, from 13:45 to 15:05, from 15:40 to 17:00
Thursday: Free only at the following times: from 9:00 to 10:20, from 11:05 to 12:35, from 12:40 to 17:00
Friday: Booked at the following times: from 10:20 to 10:55, from 11:20 to 12:50, from 13:25 to 13:30, from 14:40 to 15:05


Rachel is in a timezone that is one hour ahead of other participants
Isabella can clear their morning schedule from 9:00 to 9:45 (if blocked) everyday if needed
Lisa asks the meeting to be scheduled such that she has at least 10 minutes of free time before the meeting (the free time must fall within her 9am to 5pm)
Let X be the length of the longest meeting (in minutes) that can be scheduled if the meeting has to start on the hour or half hour. Also, let Y be number of possible options of such meetings. Compute X and Y and report them separated by a comma (e.g., 45, 3). If X is 0, report 0, 0.

---

## LOGIC-18: Multi-Step Time Arithmetic
**Domain:** Temporal Reasoning / Arithmetic
**Type:** exactMatch

Let the answer to Question1 be X.

Question1: Today is 2007-06-14 (yyyy-mm-dd format) and I was born on 2005-09-14. I am M months old. Compute M. You can assume the time between the same date in two consecutive months to be 1 month. Eg: the time between 02/13/2020 and 03/13/2020 is 1 month. Your answer should be the number of months without the unit (for example, 12).

Let the answer to Question2 be Y.

Question2: Asher was born on 2013-02-14. Compute his age in days on 2015-04-14. Both dates are in yyyy-mm-dd format. Your answer should be the number of days without the unit (for example, 233).

Let the answer to Question3 be Z.

Question3: Natalie and Chris were born on 2004-Feb-18 and 2004-Dec-30 respectively. When Chris was 991 days old, how old was Natalie in days? Your answer should be the number of days without the unit (for example, 233).

Let X' = X - 11, Y' = Y - 732, and Z' = Z - 1301.

Use these values to solve Question4.

Question4: If Lily, Jenny, Dan, Emma, Joe have their exams at (times separated by ;):  17:00 (24hr); X':Y':Z' PM; 14:00 (24hr); 22:53 (24hr); 07:19 PM respectively, find the persons whose exams are strictly before the cut-off time of 07:06:19 (24hr). If a time is at a lower granularity, assume the earliest value for the missing information. Eg: if the time is 2:40 PM, assume the complete time to be 2:40:00 PM. Your answer should be an ordered list with alphabetically ordered items (for example, [answer1, answer2, ...]). If there are no valid answers, return an empty list [].

---

## LOGIC-19: Truth-Teller Identification
**Domain:** Logical Deduction / Knights and Knaves
**Type:** exactMatch

Three people — A, B, and C — each either always tell the truth or always lie. Exactly one of them is a truth-teller. A says: "B is a liar." B says: "C is a liar." C says: "A and B are both liars." Who is the truth-teller?

---

## LOGIC-20: Web of Lies — Large-Scale Truth Inference
**Domain:** Logical Deduction / Constraint Propagation
**Type:** exactMatch

In this question, assume each person either always tells the truth or always lies. Oscar says Mohamed tells the truth. Uri says Melody tells the truth. Onyx says Max lies. Micah says Mercedes lies. Audrie says only one of Shalonda, Uri and Martha tells the truth. Kandi says Inga lies. Inga says only one of Willian, Maya and Oden tells the truth. Osvaldo says Odin lies. Christie says Fletcher, Mindy and Orlando all tell the truth. Fletcher says Jim lies. Leda says exactly two of Delfina, Mandy and Osborne tells the truth. Mehran says Milton lies. Marshall says Miles tells the truth. Shalonda says Jerry, Marshall and Odysseus all tell the truth. Kristian says only one of Jaymie, Maxwell and Mona lies. Sherrie says Tamika lies. Tamika says exactly one of Lorine, Osvaldo and Odin tell the truth. Oden says Disha lies. Odysseus says Miles lies. Morgan says Oona tells the truth. Oswald says Mohamed lies. Mona says Margaret lies. Molly says Mia lies. Milton says Mehran lies. Mallory says Orla lies. Sal says exactly two of Audrie, Max and Onyx tell the truth. Maya says Disha tells the truth. Jaymie says either exactly one of Yoland, Michelle and Miriam tells the truth, or all three of them. Miguel says Meredith tells the truth. Osborne says Mandy lies. Martha says Melody lies. Conception says either exactly one of Kristian, Oona and Morgan tells the truth, or all three of them. Shaunda says exactly two of Christie, Molly and Mia tells the truth. Jim says Dallas tells the truth. Miriam says Michelle tells the truth. Mercedes says Micah lies. Meredith says Miguel tells the truth. Max says Onyx lies. Amberly says only one of Conception, Muriel and Mallory tells the truth. Orlando says Ozias lies. Oona says Morgan tells the truth. Yoland says either exactly two of Sima, Meredith and Miguel tell the truth or none of them. Mia says Molly lies. Willian says exactly two of Leda, Micah and Mercedes tells the truth. Odin says Osvaldo lies. Sima says exactly two of Sherrie, Mehran and Milton tell the truth. Dallas says exactly one of Sal, Omar and Virginia tell the truth. Delfina says Amberly, Oscar and Oswald all tell the truth. Lorine tells the truth. Michelle says Miriam tells the truth. Virginia says Omar lies. Mandy says Osborne lies. Omar says Virginia lies. Maxwell says Margaret tells the truth. Muriel says Orla tells the truth. Mindy says Ozias tells the truth. Jerry says Kandi lies. Do Inga, Miles, and Shaunda tell the truth? Your answer should be a list of three words separated by commas. Each of them must be either yes (if the person tells the truth), no (if the person lies), or unknown (if the person's truth cannot be determined). For example, <unknown, no, yes> or <yes, yes, yes>.

---

## LOGIC-21: Word Sorting Verification
**Domain:** Lexicographic Ordering / Error Detection
**Type:** exactMatch

You are an expert in word sorting. You will be provided with a list of words and the steps taken, in the form of thoughts, to arrange them in alphabetical order.
Your job is to identify the first step that was a mistake in reasoning about the order of the words. This can be misunderstanding the order of
the alphabet or getting the word or letter wrong or missing a word entirely.
Q: Sort the following words alphabetically: List: schroeder cheerful sagacious turquoise chlorine murder joust cancelling catharsis insufferable veto blare fishpond lemma chaos ionic advert cossack wahl ama
Thought 1: I should start by looking at the first letter of the words in the list. The first letter: "schroeder": "s" (19). "cheerful": "c" (3). "sagacious": "s" (19). "turquoise": "t" (20). "chlorine": "c" (3). "murder": "m" (13). "joust": "j" (10). "cancelling": "c" (3). "catharsis": "c" (3). "insufferable": "i" (9). "veto": "v" (22). "blare": "b" (2). "fishpond": "f" (6). "lemma": "l" (12). "chaos": "c" (3). "ionic": "i" (9). "advert": "a" (1). "cossack": "c" (3). "wahl": "w" (23). "ama": "a" (1).
Thought 2: We now have: (1) ["advert" ? "ama"] < (2) "blare" < (3) ["chlorine" ? "cheerful" ? "chaos" ? "cancelling" ? "catharsis" ? "cossack"] < (6) "fishpond" < (9) ["insufferable" ? "ionic"] < (10) "joust" < (12) "lemma" < (13) "murder" < (19) ["sagacious" ? "schroeder"] < (20) "turquoise" < (22) "veto" < (23) "wahl".
Thought 3: Now let's sort this subpart ["advert" ? "ama"] by looking at their second letters. The second letter: "advert": "d" (4). "ama": "m" (13).
Thought 4: We now have: (4) "advert" < (13) "ama" for the subpart. Hence, we have "advert" < "ama" < "blare" < ["chlorine" ? "cheerful" ? "chaos" ? "cancelling" ? "catharsis" ? "cossack"] < "fishpond" < ["insufferable" ? "ionic"] < "joust" < "lemma" < "murder" < ["sagacious" ? "schroeder"] < "turquoise" < "veto" < "wahl".
Thought 5: Now let's sort this subpart ["chlorine" ? "cheerful" ? "chaos" ? "cancelling" ? "catharsis" ? "cossack"] by looking at their second letters. The second letter: "chlorine": "h" (8). "cheerful": "e" (5). "chaos": "a" (1). "cancelling": "a" (1). "catharsis": "a" (1). "cossack": "o" (15).
Thought 6: We now have: (1) ["cancelling" ? "catharsis" ? "chaos"] < (5) "cheerful" < (8) "chlorine" < (15) "cossack" for the subpart. Hence, we have "advert" < "ama" < "blare" < ["cancelling" ? "catharsis" ? "chaos"] < "cheerful" < "chlorine" < "cossack" < "fishpond" < ["insufferable" ? "ionic"] < "joust" < "lemma" < "murder" < ["sagacious" ? "schroeder"] < "turquoise" < "veto" < "wahl".
Thought 7: Now let's sort this subpart ["cancelling" ? "catharsis" ? "chaos"] by looking at their third letters. The third letter: "cancelling": "c" (3). "catharsis": "t" (20). "chaos": "o" (15).
Thought 8: We now have: (3) "cancelling" < (15) "chaos" < (20) "catharsis" for the subpart. Hence, we have "advert" < "ama" < "blare" < "cancelling" < "chaos" < "catharsis" < "cheerful" < "chlorine" < "cossack" < "fishpond" < ["insufferable" ? "ionic"] < "joust" < "lemma" < "murder" < ["sagacious" ? "schroeder"] < "turquoise" < "veto" < "wahl".
Thought 9: Now let's sort this subpart ["insufferable" ? "ionic"] by looking at their second letters. The second letter: "insufferable": "u" (21). "ionic": "o" (15).
Thought 10: We now have: (15) "ionic" < (21) "insufferable" for the subpart. Hence, we have "advert" < "ama" < "blare" < "cancelling" < "chaos" < "catharsis" < "cheerful" < "chlorine" < "cossack" < "fishpond" < "ionic" < "insufferable" < "joust" < "lemma" < "murder" < ["sagacious" ? "schroeder"] < "turquoise" < "veto" < "wahl".
Thought 11: Now let's sort this subpart ["sagacious" ? "schroeder"] by looking at their second letters. The second letter: "sagacious": "a" (1). "schroeder": "c" (3).
Thought 12: We now have: (1) "sagacious" < (3) "schroeder" for the subpart. Hence, we have "advert" < "ama" < "blare" < "cancelling" < "chaos" < "catharsis" < "cheerful" < "chlorine" < "cossack" < "fishpond" < "ionic" < "insufferable" < "joust" < "lemma" < "murder" < "sagacious" < "schroeder" < "turquoise" < "veto" < "wahl".
Thought 13: I have now sorted all the words. The answer is advert ama blare cancelling catharsis chaos cheerful chlorine cossack fishpond ionic insufferable joust lemma murder sagacious schroeder turquoise veto wahl
Q: Is there a mistake in this sequence? Write "No" if there are no mistakes, or the number N if there is a mistake in Thought N.

---

## LOGIC-22: Zebra Puzzle
**Domain:** Constraint Satisfaction / Logic Grid
**Type:** exactMatch

There are 8 people next to each other in a row in positions 1, 2, 3, 4, 5, 6, 7, 8 who have the following characteristics.
Everyone is a different nationality: Chilean, Turkish, Bangladeshi, Japanese, Belarusian, Swede, Italian, Australian.
Everyone reads a different genre of books: short story, science fiction, fantasy, spiritual, history, magical realism, mystery, humor.
Everyone plays a different musical instrument: harmonica, oboe, guitar, violin, drums, flute, cello, piano.
Everyone likes a different favorite animal: starfish, beavers, kudus, eagles, otters, hippopotamuses, elk, donkeys.
Everyone likes a different fruit: oranges, blueberries, apples, bananas, strawberries, kiwis, pears, mangoes.
Everyone plays a different sport: ice hockey, baseball, table tennis, tennis, squash, badminton, cricket, basketball.
Everyone lives in a different colored house: silver, beige, purple, grey, orange, black, cyan, turquoise.
Everyone likes a different physical activity: scuba diving, base jumping, skiing, hiking, running, snorkeling, paragliding, bungee jumping.
Using the clues provided below, answer the question at the end.
Clue 1: The person who lives in the black house is the person who reads spiritual books.
Clue 2: The basketball player is somewhere in between the person who eats apples and the person who likes scuba diving in that order.
Clue 3: The person who likes skiing is somewhere to the left of the cello player.
Clue 4: The person who likes otters is the person who reads short story books.
Clue 5: The Turkish is the drums player.
Clue 6: The person who lives in the cyan house is next to the badminton player.
Clue 7: The person who likes bungee jumping is next to the ice hockey player.
Clue 8: The guitar player is immediately to the left of the person at the 6th position.
Clue 9: The person who reads humor books is immediately to the left of the person who likes donkeys.
Clue 10: The piano player is the person who eats apples.
Clue 11: The flute player is the person who likes elk.
Clue 12: The person who likes beavers is somewhere to the left of the person who reads magical realism books.
Clue 13: The person who likes eagles is next to the person who lives in the black house.
Clue 14: The person who lives in the orange house is immediately to the left of the oboe player.
Clue 15: The harmonica player is at one of the ends.
Clue 16: The Australian is next to the harmonica player.
Clue 17: The person who eats mangoes is next to the person who likes bungee jumping.
Clue 18: The person who lives in the turquoise house is immediately to the left of the person who reads spiritual books.
Clue 19: The guitar player is the person who eats blueberries.
Clue 20: The person at the 7th position is the person who likes skiing.
Clue 21: The Bangladeshi is at one of the ends.
Clue 22: The person at the 8th position is next to the person who lives in the cyan house.
Clue 23: The person who reads spiritual books is next to the Japanese.
Clue 24: The person who lives in the beige house is next to the Turkish.
Clue 25: The person who eats kiwis is immediately to the left of the person who likes elk.
Clue 26: The squash player is the person who likes elk.
Clue 27: The person who likes base jumping is at one of the ends.
Clue 28: The person who reads history books is next to the person who lives in the cyan house.
Clue 29: The person who eats bananas is the basketball player.
Clue 30: The person who lives in the grey house is the Belarusian.
Clue 31: The person who lives in the grey house is the person who eats pears.
Clue 32: The person who eats apples is the person who likes hiking.
Clue 33: The person who eats oranges is at one of the ends.
Clue 34: The person who likes paragliding is immediately to the left of the person who reads fantasy books.
Clue 35: The person who likes running is somewhere to the left of the person who reads humor books.
Clue 36: The person who reads magical realism books is somewhere in between the person who likes bungee jumping and the baseball player in that order.
Clue 37: The person who lives in the black house is the Australian.
Clue 38: The violin player is the person who likes paragliding.
Clue 39: The badminton player is the person who likes bungee jumping.
Clue 40: The Swede is immediately to the left of the person who lives in the silver house.
Clue 41: The person who likes starfish is immediately to the left of the person who likes hiking.
Clue 42: The person who likes donkeys is the Swede.
Clue 43: The person who likes kudus is somewhere to the left of the person who likes scuba diving.
Clue 44: The drums player is immediately to the left of the person who lives in the cyan house.
Clue 45: The harmonica player is the person who reads short story books.
Clue 46: The person who likes elk is the Chilean.
Clue 47: The person who likes elk is somewhere to the left of the person who reads science fiction books.
Clue 48: The table tennis player is somewhere in between the person at the 2nd position and the person who reads humor books in that order.
Clue 49: The person who likes scuba diving is the Swede.
Clue 50: The cricket player is at one of the ends.
Clue 51: The Chilean is next to the cello player.
Clue 52: The person who likes skiing is immediately to the left of the person who eats pears.

Question: What position is the person who likes beavers at?
