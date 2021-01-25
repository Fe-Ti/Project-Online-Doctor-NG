%:- module(kbase_deseases).

:- use_module(library(lists)).


% список симптомов для выдачи клиенту

список_симптомов([
                 "гипертония",
                   "отек на двух ногах",
                   "кашель",
                   "насморк",
                   "высокая температура",
                   "отёчность_лица",
                   "расширение поверхностных вен нижних конечностей у пациента или в семейном намнезе",
                   "отек на одной ноге",
                   "принимает препараты из группы БКК",
                   "отеки постоянные/не проходят после сна и отдыха",
				   "боль в животе",
				   "боль в верхних отделах желудочно-кишечного тракта",
				   "тошнота,рвота, боль в области эпигастрия",
				   "изжога, жжение за грудиной и отрыжка",
				   "острейшая боль, складывает человека пополам",
				   "боль в нижнем отделе желудочно-кишечного тракта",
				   "сопровождается отрыжкой и метеоризмом",
				   "боль проходит после акта дефекации",
				   "боль исчезает при исключении злаковых продуктов, сопровождается диареей, тошнотой, вздутием и потерей веса",
				   "запоры",
				   "циклические боли, раз в месяц, дискомфорт, сопровождаются менструацией",
				   "сопровождается болезненными мочеиспусканиями и болью в надлобковой области",
				   "боль сопровождается диареей, стулом с примесью крови, слизи, истощение организма"
                 ]).

% или вот так его можно записать
%    список_симптомов(["гипертония","отек на двух ногах","кашель","насморк","высокая температура", "отёчность_лица", "расширение поверхностных вен нижних конечностей у пациента или в семейном намнезе","отек на одной ноге","принимает препараты из группы БКК","отеки постоянные/не проходят после сна и отдыха"]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% База знаний "класс заболевания - симптомы"
%

заболевание_для_кардиолога(Симптомы):-
    member("гипертония", Симптомы);
    member("отек на двух ногах", Симптомы).

орви(Симптомы) :-
    member("кашель", Симптомы);
    member("насморк", Симптомы);
%    member("nose", Симптомы);
    member("высокая температура", Симптомы).

аллергия(Симптомы):-
	member("отёчность_лица", Симптомы),
	\+ member("расширение поверхностных вен нижних конечностей у пациента или в семейном намнезе",Симптомы),
	\+ member("отек на ноге", Симптомы).

заболевание_для_флеболога_или_хирурга(Симптомы):-
	member("отек на ноге", Симптомы);
	member("расширение поверхностных вен нижних конечностей у пациента или в семейном намнезе",Симптомы).

заболевание_для_терапевта(Симптомы):-
	member("принимает препараты из группы БКК", Симптомы).

заболевание_для_нефролога(Симптомы):-
	member("отеки постоянные/не проходят после сна и отдыха", Симптомы),
	member("отечность лица",Симптомы).
	
срочно_в_больницу(Симптомы):-
	member("боль в животе", Симптомы);
	member("острейшая боль, складывает человека пополам", Симптомы).

заболевание_для_гастроэнтеролога(Симптомы):-
	member("боль в животе", Симптомы);
	member("боль в верхних отделах желудочно-кишечного тракта", Симптомы);
	member("тошнота,рвота, боль в области эпигастрия", Симптомы);
	member("изжога, жжение за грудиной и отрыжка", Симптомы);
	member("боль в нижнем отделе желудочно-кишечного тракта", Симптомы);
	member("сопровождается отрыжкой и метеоризмом", Симптомы);
	member("боль проходит после акта дефекации", Симптомы);
	member("боль исчезает при исключении злаковых продуктов, сопровождается диареей, тошнотой, вздутием и потерей веса", Симптомы);
	member("боль сопровождается диареей, стулом с примесью крови, слизи, истощение организма", Симптомы);
	member("запоры", Симптомы).
	

заболевание_для_гинеколога(Симптомы):-
	member("циклические боли, раз в месяц, дискомфорт, сопровождаются менструацией", Симптомы),
	member("боль в нижнем отделе желудочно-кишечного тракта", Симптомы);
	member("боль в животе", Симптомы).
	
заболевание_для_уролога(Симптомы):-
	member("сопровождается болезненными мочеиспусканиями и болью в надлобковой области", Симптомы),
	member("боль в нижнем отделе желудочно-кишечного тракта", Симптомы);
	member("боль в животе", Симптомы).


