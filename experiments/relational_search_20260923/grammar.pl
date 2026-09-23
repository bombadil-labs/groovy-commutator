% A finite grammar, not unrestricted program synthesis.
% Witnesses are externally validated pairs with different fixed-target futures.
:- dynamic candidate/3, done/1, rejected/2, witness/3.
:- use_module(library(solution_sequences)).

rgs(0, _, []).
rgs(N, Max, [X|Xs]) :-
    N > 0, Upper is Max+1, between(0, Upper, X),
    Next is max(Max,X), Rest is N-1, rgs(Rest, Next, Xs).

refines(P, T) :-
    \+ (nth0(I,P,X), nth0(J,P,X), nth0(I,T,A), nth0(J,T,B), A =\= B).

encoders(T, Ps) :-
    length(T,N), Rest is N-1,
    findall([0|Xs], (rgs(Rest,0,Xs), refines([0|Xs],T)), Ps).

install(Rows) :-
    retractall(candidate(_,_,_)), retractall(done(_)),
    retractall(rejected(_,_)), retractall(witness(_,_,_)),
    nb_setval(visits,0), nb_setval(comparisons,0),
    forall(member([I,W,P],Rows), assertz(candidate(I,W,P))).

bump(K) :- nb_getval(K,N), M is N+1, nb_setval(K,M).
same_codes(_, [], []).
same_codes(P, [A|As], [B|Bs]) :-
    nth0(A,P,X), nth0(B,P,X), same_codes(P,As,Bs).

conflict(P, Id) :-
    witness(Id,A,B), bump(comparisons), same_codes(P,A,B).

live(Mode,I,W) :-
    candidate(I,W,P), \+ done(I), \+ rejected(I,_), bump(visits),
    (Mode = guided, once(conflict(P,Id)) -> assertz(rejected(I,Id)), fail ; true).

% Return the cheapest surviving tier, at most Limit entries in canonical order.
% W is a cost-equivalent integer, installed in decreasing order by Python.
batch(Mode,Limit,Is) :-
    (once(live(Mode,First,W)) ->
        More is Limit-1,
        findnsols(More,I,(candidate(I,W,_), I > First, live_at(Mode,I,W)),Tail),
        Is=[First|Tail]
    ; Is=[]).

live_at(Mode,I,W) :- live(Mode,I,W).
mark(I) :- candidate(I,_,_), \+ done(I), assertz(done(I)).
add_witness(Id,A,B) :- \+ witness(Id,_,_), assertz(witness(Id,A,B)).
stats(V,C,R) :-
    nb_getval(visits,V), nb_getval(comparisons,C),
    findall([I,Id],rejected(I,Id),R).
