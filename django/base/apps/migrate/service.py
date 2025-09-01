from helpers.base_service import BaseService
from helpers.base_model import BaseModel
from helpers.security_validator import SecurityValidator
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from datetime import datetime
from utils.json_util import JsonUtil


class MainService(BaseService):
    @staticmethod
    def academic_year(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_academic_year import EduAcademicYear, EduAcademicYearData
        from models.edu_semester import EduSemester, EduSemesterData

        academic_year = JsonUtil.read("v2_data/quamus_lms.school_academic_year.json")
        semester = JsonUtil.read("v2_data/quamus_lms.school_semester.json")
        academic_year = sorted(academic_year, key=lambda x: x["year"])
        print("semester", semester)
        input_academic_year_data = []
        input_semester_data = []
        for i in academic_year:
            print(i)
            selected_semester = [
                item
                for item in semester
                if item.get("academic_year_id") == i.get("_id")
            ]
            fields = MainService.academic_year__fields(i.get("year"))
            new_academic_year_data = EduAcademicYearData(
                _id=ObjectId(i.get("_id")),
                name=fields["name"],
                short_name=fields["short_name"],
                year=i["year"],
                start_date=datetime.strptime(fields["start_date"], "%Y-%m-%d"),
                end_date=datetime.strptime(fields["end_date"], "%Y-%m-%d"),
                semester_ids=[
                    ObjectId(selected_semester[0]["_id"]),
                    ObjectId(selected_semester[1]["_id"]),
                ],
            )
            input_academic_year_data.append(new_academic_year_data)

            semester_doc = [
                EduSemesterData(
                    _id=ObjectId(selected_semester[idx]["_id"]),
                    academic_year_id=new_academic_year_data._id,
                    semester_no=idx + 1,
                    name="Ganjil" if idx + 1 == 1 else "Genap",
                    start_date=MainService.academic_year__semester_range(
                        i.get("year"), idx + 1
                    ).get("start_date"),
                    end_date=MainService.academic_year__semester_range(
                        i.get("year"), idx + 1
                    ).get("end_date"),
                )
                for idx, j in enumerate(fields["semester_ids"])
            ]
            input_semester_data = [*input_semester_data, *semester_doc]

        if input_academic_year_data:
            EduAcademicYear().insert_many(input_academic_year_data)
        if input_semester_data:
            EduSemester().insert_many(input_semester_data)

        return {
            "message": None,
        }

    @staticmethod
    def academic_year__fields(year):
        name = f"{int(year)}/{int(year)+1}"
        short_name = f"{str(year)[-2:]}{str(int(year)+1)[-2:]}"
        start_date = f"{int(year)}-07-01"
        end_date = f"{int(year)+1}-06-30"
        semester_ids = [ObjectId(), ObjectId()]

        return {
            "name": name,
            "short_name": short_name,
            "start_date": start_date,
            "end_date": end_date,
            "semester_ids": semester_ids,
        }

    @staticmethod
    def academic_year__semester_range(year, semester_number):
        if semester_number == 1:
            start_date = datetime.strptime(f"{year}-07-01", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
        else:
            start_date = datetime.strptime(f"{year+1}-01-01", "%Y-%m-%d")
            end_date = datetime.strptime(f"{year+1}-06-30", "%Y-%m-%d")

        return {"start_date": start_date, "end_date": end_date}

    @staticmethod
    def subject(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_subject import EduSubject, EduSubjectData

        subject = JsonUtil.read("v2_data/quamus_lms.school_subject.json")
        input_data = []
        for idx, i in enumerate(subject, start=1):
            new_subject_data = EduSubjectData(
                _id=ObjectId(i.get("_id")),
                name=i.get("name"),
                short_name="",
                sequence=idx,
                thumbnail_img=(
                    i.get("image_url")[0] if len(i.get("image_url")) > 0 else None
                ),
                is_catalogue=False,
                is_active=True,
            )
            input_data.append(new_subject_data)
        if input_data:
            EduSubject().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def stage(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_stage import EduStage, EduStageData

        # new_stage_data = EduStageData(
        #     _id=ObjectId("63be0e910fce905c08673dbf"),
        #     group_id=ObjectId("68afd16df91014a79db8a095"),
        #     name="Sekolah Menengah Atas",
        #     short_name="SMA",
        #     origin="domestic",
        # )
        # EduStage().insert_one(new_stage_data)

        return {
            "message": None,
        }

    @staticmethod
    def stage_level(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_stage_level import EduStageLevel, EduStageLevelData

        subject = JsonUtil.read("v2_data/quamuslms.edu_stage_level.json")
        input_data = []
        for i in subject:
            new_stage_level_data = EduStageLevelData(
                _id=ObjectId(i.get("_id").get("$oid")),
                degree_id=(
                    ObjectId(i.get("degree_id").get("$oid"))
                    if i.get("degree_id")
                    else None
                ),
                group_id=ObjectId(i.get("group_id").get("$oid")),
                name=i.get("name"),
                sequence=i.get("sequence"),
                is_final=i.get("is_final"),
                is_extension=i.get("is_extension"),
            )
            input_data.append(new_stage_level_data)
        if input_data:
            EduStageLevel().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def stage_group(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_stage_group import EduStageGroup
        from models.edu_stage_level import EduStageLevel
        from models.edu_stage import EduStage

        group_data = EduStageGroup().find()
        level_data = EduStageLevel().find()
        stage_data = EduStage().find()

        update_data = []
        for i in group_data:
            print(i)
            level_ids = [
                ObjectId(item.get("_id"))
                for item in level_data
                if item.get("group_id") == i.get("_id")
            ]
            stage_ids = [
                ObjectId(item.get("_id"))
                for item in stage_data
                if item.get("group_id") == i.get("_id")
            ]
            update_data.append(
                {
                    "_id": ObjectId(i.get("_id")),
                    "set_data": {"level_ids": level_ids, "stage_ids": stage_ids},
                }
            )
        if update_data:
            EduStageGroup().update_many_different_data(update_data)

        return {
            "message": None,
        }

    @staticmethod
    def subject_level(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.edu_subject import EduSubject
        from models.edu_subject_level import EduSubjectLevel, EduSubjectLevelData
        from models.edu_stage_level import EduStageLevel

        subject_data = EduSubject().find()
        subject_data = {item.get("_id"): item for item in subject_data}
        level_data = EduStageLevel().find()
        level_data = {item.get("_id"): item for item in level_data}
        subject_level = JsonUtil.read("v2_data/quamus_lms.school_subject_level.json")
        input_data = []
        for i in subject_level:
            print(i)
            selected_subject = subject_data.get(i.get("subject_id"))
            for j in i.get("level_id"):
                selected_level = level_data.get(j)
                new_subject_level_data = EduSubjectLevelData(
                    subject_id=ObjectId(i.get("subject_id")),
                    level_id=ObjectId(j),
                    name=f"{selected_subject.get('name')} {selected_level.get('name')}",
                    thumbnail_img=i.get("thumbnail_img"),
                    subject_seq=selected_subject.get("sequence"),
                    is_catalogue=False,
                    is_active=True,
                )
                input_data.append(new_subject_level_data)

        if input_data:
            EduSubjectLevel().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def quran_chapter(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_chapter import QuranChapter, QuranChapterData

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_chapter.json")
        input_data = []
        for i in json_data:
            print(i)
            new_quran_chapter_data = QuranChapterData(
                sequence=i.get("_id"),
                name={
                    "latin": i.get("name").get("latin_simple"),
                    "arabic": i.get("name").get("arabic"),
                },
                translation={
                    "en": i.get("translation").get("en"),
                    "id": i.get("translation").get("id"),
                },
                description=i.get("description"),
                verse_count=i.get("verses_count"),
                page_from=i.get("page").get("from"),
                page_to=i.get("page").get("to"),
                verse_seq_from=i.get("verse_id").get("from"),
                verse_seq_to=i.get("verse_id").get("to"),
            )
            input_data.append(new_quran_chapter_data)
        if input_data:
            print(input_data)
            QuranChapter().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def quran_juz(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_juz import QuranJuz, QuranJuzData
        from models.quran_chapter import QuranChapter

        chapter_data = QuranChapter().find()

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_juz.json")
        input_data = []
        for i in json_data:
            print(i)
            selected_chapter = [
                item
                for item in chapter_data
                if item.get("sequence") in i.get("chapter_id")
            ]
            new_quran_juz_data = QuranJuzData(
                name=f"Juz {i.get('_id')}",
                sequence=i.get("_id"),
                chapter_ids=[ObjectId(item.get("_id")) for item in selected_chapter],
                chapter_seq_from=i.get("chapter_id")[0],
                chapter_seq_to=i.get("chapter_id")[-1],
                verse_seq_from=i.get("verse_id").get("from"),
                verse_seq_to=i.get("verse_id").get("to"),
                page_seq_from=i.get("page").get("from"),
                page_seq_to=i.get("page").get("to"),
                verse_count=i.get("verse_id").get("to")
                - i.get("verse_id").get("from")
                + 1,
            )
            input_data.append(new_quran_juz_data)
        if input_data:
            print(input_data)
            QuranJuz().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def quran_page(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_page import QuranPage, QuranPageData
        from models.quran_juz import QuranJuz

        juz_data = QuranJuz().find()

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_page.json")
        input_data = []
        for i in json_data:
            print(i)
            selected_juz = [
                item
                for item in juz_data
                if i.get("_id") >= item.get("page_seq_from")
                and i.get("_id") <= item.get("page_seq_to")
            ]
            if selected_juz:
                selected_juz = selected_juz[0]
                new_quran_page_data = QuranPageData(
                    juz_id=ObjectId(selected_juz.get("_id")),
                    juz_seq=selected_juz.get("sequence"),
                    name=f"Hal {i.get('_id')}",
                    sequence=i.get("_id"),
                    verse_count=i.get("verse_count"),
                    verse_seq_from=i.get("verse_id").get("from"),
                    verse_seq_to=i.get("verse_id").get("to"),
                    line_ids=[],
                )
                input_data.append(new_quran_page_data)
        if input_data:
            print(input_data)
            QuranPage().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def quran_line(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_line import QuranLine, QuranLineData
        from models.quran_page import QuranPage
        from models.quran_juz import QuranJuz

        page_data = QuranPage().find()
        page_data = {item.get("sequence"): item for item in page_data}
        juz_data = QuranJuz().find()
        juz_data = {item.get("sequence"): item for item in juz_data}

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_line.json")
        update_page_data = {}
        input_data = []
        for i in json_data:
            selected_page = page_data.get(i.get("page_number"))
            chapter_name = {"latin": "", "arabic": ""}
            chapter_seq = None
            if i.get("line") == 1:
                chapter_name = {
                    "latin": i.get("page_info").get("chapter_name").get("latin_simple"),
                    "arabic": i.get("page_info").get("chapter_name").get("arabic"),
                }
                chapter_seq = i.get("page_info").get("chapter_id")
            elif i.get("type") == "title":
                chapter_name["arabic"] = i.get("chapter_name")
            new_quran_line_data = QuranLineData(
                name=f"{selected_page.get('name')} Baris {i.get('line')}",
                sequence=i.get("line"),
                page_id=ObjectId(selected_page.get("_id")),
                page_seq=selected_page.get("sequence"),
                word_ids=[],
                chapter_name=chapter_name,
                chapter_seq=chapter_seq,
                juz_id=ObjectId(selected_page.get("juz_id")),
                juz_seq=selected_page.get("juz_seq"),
                is_word=i.get("type") != "title",
                is_title=i.get("type") == "title",
                is_first_line=i.get("line") == 1,
                is_last_line=i.get("last_line"),
            )
            input_data.append(new_quran_line_data)
            update_page_data.setdefault(selected_page.get("_id"), [])
            update_page_data[selected_page.get("_id")].append(new_quran_line_data._id)
        if input_data:
            print(input_data)
            QuranLine().insert_many(input_data)
        if update_page_data:
            update_data = []
            for k, v in update_page_data.items():
                update_data.append({"_id": ObjectId(k), "set_data": {"line_ids": v}})
            QuranPage().update_many_different_data(update_data)
        return {
            "message": None,
        }

    @staticmethod
    def quran_verse(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_verse import QuranVerse, QuranVerseData
        from models.quran_juz import QuranJuz
        from models.quran_chapter import QuranChapter
        from models.quran_page import QuranPage

        juz_data = QuranJuz().find()
        juz_data = {item.get("sequence"): item for item in juz_data}
        chapter_data = QuranChapter().find()
        chapter_data = {item.get("sequence"): item for item in chapter_data}
        page_data = QuranPage().find()
        page_data = {item.get("sequence"): item for item in page_data}

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_verse.json")
        input_data = []
        for i in json_data:
            selected_chapter = chapter_data.get(i.get("chapter_id"))
            selected_juz = juz_data.get(i.get("meta").get("juz"))
            selected_page = page_data.get(i.get("meta").get("page"))
            new_quran_verse_data = QuranVerseData(
                name=f"{selected_chapter.get('name').get('latin')} Ayat {i.get('number')}",
                sequence=i.get("_id"),
                verse_no=i.get("number"),
                juz_id=ObjectId(selected_juz.get("_id")),
                juz_seq=selected_juz.get("sequence"),
                chapter_id=ObjectId(selected_chapter.get("_id")),
                chapter_seq=selected_chapter.get("sequence"),
                page_id=ObjectId(selected_page.get("_id")),
                page_seq=selected_page.get("sequence"),
                arabic=i.get("arabic"),
                translation=i.get("translation"),
            )
            input_data.append(new_quran_verse_data)
        if input_data:
            QuranVerse().insert_many(input_data)
        return {
            "message": None,
        }

    @staticmethod
    def quran_word(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_word import QuranWord, QuranWordData
        from models.quran_chapter import QuranChapter
        from models.quran_line import QuranLine
        from models.quran_verse import QuranVerse
        from utils.arabic_similarity import similarity_score

        chapter_data = QuranChapter().find()
        chapter_data = {item.get("sequence"): item for item in chapter_data}
        verse_data = QuranVerse().find()
        verse_data = {item.get("sequence"): item for item in verse_data}
        line_data = QuranLine().find()
        line_data = {
            f"{item.get('page_seq')}-{item.get('sequence')}": item for item in line_data
        }

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_line.json")
        json_kemenag_data = JsonUtil.read("v2_data/kemenag.json")
        allowed_chapter = [1, 114]
        input_data = []
        update_verse_data = {}
        update_line_data = {}
        for i in json_data:
            if i.get("type") == "word":
                selected_line = line_data.get(f"{i.get('page_number')}-{i.get('line')}")
                for j in i.get("word"):
                    # if j.get("chapter_id") in allowed_chapter:
                    if j.get("type") == "word":
                        score = similarity_score(
                            j.get("text"),
                            json_kemenag_data.get(str(j.get("chapter_id"))).get(
                                str(j.get("verse_number"))
                            )[j.get("word_order") - 1],
                        )
                        if score < 50:
                            print(
                                j.get("text"),
                                ":",
                                json_kemenag_data.get(str(j.get("chapter_id"))).get(
                                    str(j.get("verse_number"))
                                )[j.get("word_order") - 1],
                                j.get("chapter_id"),
                                j.get("verse_number"),
                                j.get("word_order"),
                                score,
                            )

                        # print(j, score)

                    selected_chapter = chapter_data.get(j.get("chapter_id"))
                    selected_verse = verse_data.get(j.get("verse_id"))

                    # print(selected_chapter)
                    print(j)
                    new_quran_word_data = QuranWordData(
                        code=j.get("_id"),
                        juz_id=ObjectId(selected_line.get("juz_id")),
                        juz_seq=selected_line.get("juz_seq"),
                        chapter_id=ObjectId(selected_chapter.get("_id")),
                        chapter_seq=selected_chapter.get("sequence"),
                        page_id=ObjectId(selected_line.get("page_id")),
                        page_seq=selected_line.get("page_seq"),
                        line_id=ObjectId(validated_data.get("line_id")),
                        line_seq=selected_line.get("sequence"),
                        verse_id=ObjectId(selected_verse.get("_id")),
                        verse_seq=selected_verse.get("sequence"),
                        verse_no=selected_verse.get("verse_no"),
                        sequence=j.get("word_order"),
                        chapter_name=selected_chapter.get("name").get("latin"),
                        name=f"{selected_chapter.get('name').get('latin')} Ayat {selected_verse.get('verse_no')}",
                        arabic_madinah=(
                            j.get("text") if j.get("type") == "word" else None
                        ),
                        arabic_kemenag=(
                            json_kemenag_data.get(str(j.get("chapter_id"))).get(
                                str(j.get("verse_number"))
                            )[j.get("word_order") - 1]
                            if j.get("type") == "word"
                            else None
                        ),
                        last_line=j.get("last_line"),
                        last_verse_page=j.get("last_verse_page"),
                        is_word=j.get("type") == "word",
                        is_end=j.get("type") != "word",
                    )
                    input_data.append(new_quran_word_data)
                    if j.get("type") == "word":
                        update_verse_data.setdefault(selected_verse.get("_id"), [])
                        update_verse_data[selected_verse.get("_id")].append(
                            new_quran_word_data._id
                        )
                    update_line_data.setdefault(selected_line.get("_id"), [])
                    update_line_data[selected_line.get("_id")].append(
                        new_quran_word_data._id
                    )
        if input_data:
            print(input_data)
            QuranWord().insert_many(input_data)
        if update_verse_data:
            update_data = []
            for k, v in update_verse_data.items():
                update_data.append({"_id": ObjectId(k), "set_data": {"word_ids": v}})
            print(update_data)
            QuranVerse().update_many_different_data(update_data)
        if update_line_data:
            update_data = []
            for k, v in update_line_data.items():
                update_data.append({"_id": ObjectId(k), "set_data": {"word_ids": v}})
            print(update_data)
            QuranLine().update_many_different_data(update_data)
        return {
            "message": None,
        }

    @staticmethod
    def export_quran_words(json_data, dst_path="v2_data/quran_words_by_surah.json"):
        from collections import defaultdict
        import json

        """
        Input: json_data = list of verse dicts, masing-masing:
        {
            'chapter_id': int,
            'number': int,             # nomor ayat dalam surat
            'words': [ { 'word': int, 'arabic_styled': str, 'arabic_normal': str, ... }, ... ]
        }

        Output file JSON: {"NO_SURAT":{"NO_AYAT":["WORD 1","WORD 2", ...]}}
        """
        out = defaultdict(dict)  # {surah(str): {ayah(str): [words...]}}

        for verse in json_data:
            try:
                surah = str(verse["chapter_id"])
                ayah = str(verse["number"])
                words = verse.get("words", [])

                # urutkan sesuai urutan kata di ayat
                words_sorted = sorted(words, key=lambda w: w.get("word", 0))

                # ambil tulisan arab; prefer arabic_styled, fallback ke arabic_normal
                token_list = []
                for w in words_sorted:
                    token = w.get("arabic_styled") or w.get("arabic_normal") or ""
                    if token:
                        token_list.append(token)

                out[surah][ayah] = token_list
            except Exception as e:
                # Kalau ada verse yang datanya tidak lengkap, skip atau bisa log
                # print(f"Skip verse karena error: {e}")
                continue

        # simpan ke file
        with open(dst_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        return out

    @staticmethod
    def quran_verse(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_verse import QuranVerse
        import json

        src_file = "v2_data/quamus_lms.quran_verse.json"
        with open(src_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        result = MainService.export_quran_words(
            json_data, dst_path="quran_words_by_surah.json"
        )

        return {
            "message": None,
        }

    @staticmethod
    def template(model: BaseModel, validated_data, extra, user, headers_dict=None):
        from models.quran_juz import QuranJuz, QuranJuzData

        json_data = JsonUtil.read("v2_data/quamus_lms.quran_juz.json")
        for i in json_data:
            print(i)
        return {
            "message": None,
        }
