(define (domain boxman)
    (:requirements :strips :typing :equality)
    (:types physob location)
    (:constants PER - physob)  ; 推箱子的人

    (:predicates
        (at ?x - physob ?loc - location)  ; x在位置loc
        (clear ?loc - location)           ; 位置loc上没有箱子，但可能有人
        (left ?loc1 ?loc2 - location)       ; 位置loc1在loc2的左边且相邻
        (down ?loc1 ?loc2 - location)      ; 位置loc1在loc2的下面且相邻
    )

    (:action move  ; 推箱子的人从from走到to
        :parameters (?from ?to - location)
        :precondition (and
            (at PER ?from)
            (clear ?to)
            (or 
                (left ?from ?to) (left ?to ?from)
                (down ?from ?to) (down ?to ?from)
            )
        )
        :effect (and
            (at PER ?to)
            (not (at PER ?from))
        )
    )

    (:action push  ; 推箱子的人目前在pxy，他把在from处的箱子推到位置to
        :parameters (?box - physob ?pxy ?from ?to - location)
        :precondition (and
            (not (= ?box PER))
            (at ?box ?from)
            (at PER ?pxy)
            (clear ?to)
            (or  ;
                (and (left ?pxy ?from) (left ?from ?to))           ; 向右推
                (and (left ?to ?from) (left ?from ?pxy))     ; 向左推
                (and (down ?pxy ?from) (down ?from ?to))   ; 向上推
                (and (down ?to ?from) (down ?from ?pxy))   ; 向下推
            )
        )
        :effect (and
            (not (at PER ?pxy))
            (not (at ?box ?from))
            (clear ?from)     
            (at PER ?from)     
            (at ?box ?to)      
            (not (clear ?to))  
        )
    )
)
