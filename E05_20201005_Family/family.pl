/* facts */

/* gender */
male('George').
male('Philip').
male('Spencer').
male('Charles').
male('Mark').
male('Andrew').
male('Edward').
male('William').
male('Harry').
male('Peter').
male('James').
female('Mum').
female('Kydd').
female('Elizabeth').
female('Margaret').
female('Diana').
female('Anne').
female('Sarah').
female('Sophie').
female('Zara').
female('Beatrice').
female('Eugenie').
female('Louise').
female('Charlotte').

/* child */
child('Elizabeth','George').
child('Elizabeth','Mum').
child('Margaret','George').
child('Margaret','Mum').
child('Diana','Spencer').
child('Diana','Kydd').
child('Charles','Elizabeth').
child('Charles','Philip').
child('Anne','Elizabeth').
child('Anne','Philip').
child('Andrew','Elizabeth').
child('Andrew','Philip').
child('Edward','Elizabeth').
child('Edward','Philip').
child('William','Diana').
child('William','Charles').
child('Harry','Diana').
child('Harry','Charles').
child('Peter','Anne').
child('Peter','Mark').
child('Zara','Anne').
child('Zara','Mark').
child('Charlotte','William').
child('Beatrice','Andrew').
child('Beatrice','Sarah').
child('Eugenie','Andrew').
child('Eugenie','Sarah').
child('Louise','Edward').
child('Louise','Sophie').
child('James','Edward').
child('James','Sophie').

/* rules */
parent(X,Y) :- child(Y,X).
father(X,Y) :- child(Y,X), male(X).
mother(X,Y) :- child(Y,X), female(X).
husband(X,Y) :- female(Y), male(X), father(X,Z), mother(Y,Z).
wife(X,Y) :- male(Y), female(X), father(X,Z), mother(Y,Z).
spouse(X,Y) :- husband(X,Y) ; wife(Y,X).
son(X,Y) :- child(X,Y), male(X).
daughter(X,Y) :- child(X,Y), female(X).
sibling(X,Y) :- child(X,Z), child(Y,Z), X \== Y.
brother(X,Y) :- sibling(X,Y), male(X).
sister(X,Y) :- sibling(X,Y), female(X).
grandfather(X,Y) :- child(Y,Z), father(X,Z).
grandmother(X,Y) :- child(Y,Z), mother(X,Z).
grandchild(X,Y) :- child(X,Z), child(Z,Y).
grandparent(X,Y) :- parent(X,Z), parent(Z,Y).
greatGrandparent(X,Y) :- grandparent(X,Z), parent(Z,Y).
ancestor(X,Y) :- parent(X,Y). % Base
ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y). % Recursion
aunt(X,Y) :- grandparent(Z,Y), parent(Z,X), \+(mother(X,Y)), female(X).
uncle(X,Y) :- grandparent(Z,Y), parent(Z,X), \+(father(X,Y)), male(X).
%% the husband of your sister or brother
%% or the brother of your husband or wife
%% or the man who is married to the sister
%% or brother of your wife or husband
brotherInLaw(X,Y) :- (husband(X,Z), sister(Z,Y)) ; (brother(X,Z), husband(Z,Y)); (brother(X,Z), wife(Z,Y)).
sisterInLaw(X,Y) :- (wife(X,Z), brother(Z,Y)) ;(sister(X,Z), husband(Z,Y)); (sister(X,Z), wife(Z,Y)).
%% cousins
firstCousin(X,Y) :- grandparent(Z,X), grandparent(Z,Y), X \== Y, \+(sibling(X,Y)).
distance(X,Y,0) :- X = Y.
distance(X,Y,1) :- child(Y,X).
distance(X,Y,M) :- child(Z,X), M1 is M-1, distance(Z,Y,M1).
%%mthCousin(X,Y,1) :- firstCousin(X,Y).
%%mthCousin(X,Y,M) :- M1 is M+1, distance(Z,X,M1), distance(Z,Y,M1), X \== Y,
					%%distance(A,X,M), distance(B,Y,M), A \= B, parent(Z,A), parent(Z,B).
mthCousinNremoved(X,Y,M,N) :- M1 is M+N+1, distance(Z,Y,M1), M2 is M+1, distance(Z,X,M2), X \== Y,
				M4 is M+1, distance(A,Y,M4), M3 is M, distance(B,X,M3), parent(Z,A), parent(Z,B), A \== B.