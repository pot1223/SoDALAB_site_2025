from flask import Blueprint, render_template
from apps.app import db
from apps.models import (
    aboard_publication, domestic_publication,
    aboard_conference, domestic_conference, member_spec,
    present_member, past_member, home_content, activity_photo, home_photo, project_photo
)

from flask import request, redirect
from flask import  url_for
from apps.app import supabase
from flask import current_app


soda = Blueprint(
    "soda",
    __name__,
    template_folder="templates",
    static_folder = "static",
)


@soda.route("/")
def index():
    home_photos_db = home_photo.query.order_by(home_photo.id).all()
    home_contents = home_content.query.order_by(home_content.id).all()
    home_photos_with_urls = []
    for photo in home_photos_db:
        # 2. 이미지 파일명이 실제 존재하는지 체크 (방어 코드)
        if photo.home_image:
            res = supabase.storage.from_('home-images').get_public_url(photo.home_image)
            # 만약 res가 객체로 온다면 .public_url 을 붙여야 할 수도 있음 (버전에 따라 다름)
            photo.public_image_url = res 
        else:
            photo.public_image_url = url_for('soda.static', filename='images/default.png') # 기본 이미지
            
        home_photos_with_urls.append(photo)

    return render_template("soda/home.html", home_contents = home_contents, home_photos = home_photos_with_urls )


@soda.route("/people")
def people():
    # 1. 데이터 가져오기
    # spec은 최신순(date 내림차순)이나 중요도 순으로 정렬하는 것이 좋다면 order_by를 조정하세요.
    all_specs = member_spec.query.order_by(member_spec.date.desc()).all() 
    present_members = present_member.query.order_by(present_member.id).all()

    present_members_processed = []

    for member in present_members:
        # 2. 이미지 URL 처리 (기존 코드)
        res = supabase.storage.from_('profile-images').get_public_url(member.profile_image)
        member.public_image_url = res

        # 3. [핵심] 현재 멤버(member.member)와 이름이 일치하는 스펙만 찾아서 리스트로 저장
        # member_spec 테이블의 'member' 컬럼이 학생 이름이라고 가정했습니다.
        my_specs = [spec for spec in all_specs if spec.member == member.member]
        
        # 멤버 객체에 'specs_list'라는 이름으로 리스트를 심어줍니다.
        member.specs_list = my_specs
        
        present_members_processed.append(member)

    return render_template(
        "soda/people.html",
        present_members=present_members_processed
        # member_specs는 이제 따로 넘길 필요가 없습니다. present_members 안에 들어갔으니까요.
    )

#@soda.route("/gallery")
#def gallery():
    # id 기준 오름차순 정렬 추가
    activity_photos_db = activity_photo.query.order_by(activity_photo.id).all()

    activity_photos_with_urls = []
    for photo in activity_photos_db:
        # DB에 저장된 파일 경로(photo.activity_image)로 공개 URL을 가져옵니다.
        res = supabase.storage.from_('activity-images').get_public_url(photo.activity_image)
        # photo 객체에 새 속성으로 URL 추가
        photo.public_image_url = res
        activity_photos_with_urls.append(photo)

    # URL이 추가된 리스트를 템플릿으로 전달합니다.
    return render_template("soda/gallery.html", activity_photos=activity_photos_with_urls)

@soda.route("/gallery")
def gallery():
    try:
        # 1. DB에서 데이터 가져오기
        activity_photos_db = activity_photo.query.order_by(activity_photo.id).all()

        activity_photos_with_urls = []
        for photo in activity_photos_db:
            # 2. 이미지 파일명이 실제 존재하는지 체크 (방어 코드)
            if photo.activity_image:
                res = supabase.storage.from_('activity-images').get_public_url(photo.activity_image)
                # 만약 res가 객체로 온다면 .public_url 을 붙여야 할 수도 있음 (버전에 따라 다름)
                photo.public_image_url = res 
            else:
                photo.public_image_url = url_for('soda.static', filename='images/default.png') # 기본 이미지
            
            activity_photos_with_urls.append(photo)

        return render_template("soda/gallery.html", activity_photos=activity_photos_with_urls)

    except Exception as e:
        # 에러 발생 시 브라우저 화면에 에러 내용을 찍어서 확인합니다.
        import traceback
        return f"<pre>{traceback.format_exc()}</pre>"

@soda.route("/intro")
def intro():
    return render_template("soda/intro.html")

@soda.route("/domain")
def domain():
    return render_template("soda/domain.html")

@soda.route("/prof")
def prof():
    return render_template("soda/prof.html")

@soda.route("/contact")
def contact():
    return render_template("soda/contact.html")

@soda.route("/home")
def home():
    home_photos_db = home_photo.query.order_by(home_photo.id).all()
    home_contents = home_content.query.order_by(home_content.id).all()
    home_photos_with_urls = []
    for photo in home_photos_db:
        # 2. 이미지 파일명이 실제 존재하는지 체크 (방어 코드)
        if photo.home_image:
            res = supabase.storage.from_('home-images').get_public_url(photo.home_image)
            # 만약 res가 객체로 온다면 .public_url 을 붙여야 할 수도 있음 (버전에 따라 다름)
            photo.public_image_url = res 
        else:
            photo.public_image_url = url_for('soda.static', filename='images/default.png') # 기본 이미지
            
        home_photos_with_urls.append(photo)

    return render_template("soda/home.html", home_contents = home_contents, home_photos = home_photos_with_urls )

@soda.route("/project")
def project():
    projects = project_photo.query.order_by(project_photo.id).all()

    # --- 👇 이 부분이 추가/수정되었습니다 ---
    projects_with_urls = []
    for project in projects:
        # DB에 저장된 파일 경로로 Supabase에서 공개 URL을 가져옵니다.
        # 'profile-images'는 Supabase에 만드신 버킷(폴더) 이름입니다.
        res = supabase.storage.from_('project-images').get_public_url(project.project_image)

        # member 객체에 public_image_url이라는 새 속성으로 URL을 추가합니다.
        project.project_image_url = res
        projects_with_urls.append(project)
        
    return render_template("soda/project.html", project_photos=projects_with_urls )

@soda.route("/domestic")
def domestic():
    domestic_publications = domestic_publication.query.order_by(domestic_publication.id).all()
    return render_template("soda/domestic.html", domestic_publications = domestic_publications)

@soda.route("/aboard")
def aboard():
    aboard_publications = aboard_publication.query.order_by(aboard_publication.id).all()
    return render_template("soda/aboard.html", aboard_publications = aboard_publications)

@soda.route("/confer")
def confer():
    domestic_conferences = domestic_conference.query.order_by(domestic_conference.id).all()
    return render_template("soda/confer.html",  domestic_conferences =  domestic_conferences)

@soda.route("/international")
def international():
    aboard_conferences = aboard_conference.query.order_by(aboard_conference.id).all()
    return render_template("soda/inter.html", aboard_conferences = aboard_conferences)


@soda.route("/graduate")
def graduate():
    # 1. 모든 스펙 가져오기 (날짜 내림차순 등 정렬 추천)
    all_specs = member_spec.query.order_by(member_spec.date.desc()).all()
    # 2. 졸업생 가져오기
    past_members = past_member.query.order_by(past_member.id).all()

    past_members_processed = []
    for member in past_members:
        # --- 이미지 URL 처리 (기존 코드) ---
        res = supabase.storage.from_('profile-images').get_public_url(member.profile_image)
        member.public_image_url = res
        
        # --- [추가된 부분] 스펙 데이터 매칭 로직 ---
        # 졸업생 이름(member.member)과 일치하는 스펙만 필터링
        my_specs = [spec for spec in all_specs if spec.member == member.member]
        member.specs_list = my_specs # 리스트 저장
        
        past_members_processed.append(member)

    # URL과 스펙 리스트가 모두 포함된 객체 전달
    return render_template("soda/graduate.html", past_members=past_members_processed)


@soda.route("/public")
def public():
    # id 기준 오름차순 정렬 추가
    aboard_publications = aboard_publication.query.order_by(aboard_publication.id).all()
    domestic_publications = domestic_publication.query.order_by(domestic_publication.id).all()
    domestic_conferences = domestic_conference.query.order_by(domestic_conference.id).all()
    aboard_conferences = aboard_conference.query.order_by(aboard_conference.id).all()
    return render_template("soda/public.html", aboard_publications = aboard_publications,domestic_publications =domestic_publications, domestic_conferences = domestic_conferences, aboard_conferences = aboard_conferences)


@soda.route("/add", methods=["GET"])
def add_page():
    return render_template("soda/public_form.html")



# 저널 추가

@soda.route("/add_publication", methods=["POST"])
def add_publication():
    title = request.form.get("title")
    authors = request.form.get("authors")
    reference = request.form.get("reference")
    pub_type = request.form.get("pub_type")
    if pub_type == "abroad":
        new_pub = aboard_publication(
                        title=title,
                        authors=authors,
                        reference = reference,
                )
    elif pub_type == "domestic":
        new_pub = domestic_publication(
                        title=title,
                        authors=authors,
                        reference = reference,
                    )
    db.session.add(new_pub)
    db.session.commit()
    return redirect(url_for("soda.add_page"))


# 컨퍼런스 추가

@soda.route("/add_conference", methods=["POST"])
def add_conference():
    title = request.form.get("title")
    conference_name = request.form.get("conference_name")
    date = request.form.get("date")
    confer_type = request.form.get("confer_type")
    if confer_type == "abroad":
        new_confer = aboard_conference(
                        title=title,
                        conference_name=conference_name,
                        date = date,
                )
    elif confer_type == "domestic":
        new_confer = domestic_conference(
                        title=title,
                        conference_name=conference_name,
                        date = date,
                    )
    db.session.add(new_confer)
    db.session.commit()
    return redirect(url_for("soda.add_page"))


# 멤버 스펙 추가


@soda.route("/add_spec", methods=["POST"])
def add_spec():
    member = request.form.get("member")
    people = request.form.get("people")
    title = request.form.get("title")
    organi =  request.form.get("organi")
    date =  request.form.get("date")
    price = request.form.get("price")

    new_spec = member_spec(member = member,
                            people=people,
                            title=title,
                            organi= organi,
                            date= date,
                            price = price)
    db.session.add(new_spec)
    db.session.commit()
    return redirect(url_for("soda.add_page"))



# 멤버 추가
from flask import current_app, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import uuid


@soda.route("/add_member", methods=["POST"])
def add_member():
    member = request.form.get("member")
    degree = request.form.get("degree")
    department = request.form.get("department")
    email = request.form.get("email")
    interest_part = request.form.get("interest_part")
    affiliation = request.form.get("affiliation")
    member_type = request.form.get("member_type")
    profile_image_file = request.files.get('profile_image')
    # 2. 파일 처리: 파일이 존재하면 저장하고, 없으면 기본값 사용
    db_filename = 'default.jpg' # DB에 저장될 파일명 기본값


    # 파일이 정상적으로 업로드되었는지 확인
    if profile_image_file and profile_image_file.filename != '':

        # 1. 고유한 파일 경로(이름) 생성 (기존 로직 활용)
        original_filename = secure_filename(profile_image_file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
        unique_filename = str(uuid.uuid4()) + '.' + extension
        filePath = unique_filename # Supabase에 저장될 경로

        # 2. 로컬에 저장하는 대신 Supabase Storage에 업로드
        try:
            # profile_image_file.read()로 파일의 바이너리 데이터를 읽어 전달합니다.
            supabase.storage.from_('profile-images').upload(
                path=filePath,
                file=profile_image_file.read(),
                file_options={"content-type": profile_image_file.content_type}
            )
            # 성공 시, db에 저장할 파일명을 unique_filename으로 설정
            db_filename = unique_filename
        except Exception as e:
            print(f"Supabase 업로드 실패: {e}")
            # 업로드 실패 시 기본 이미지로 유지하거나 에러 처리
            db_filename = 'default.jpg'


    # 3. DB에 저장: member_type에 따라 올바른 객체 생성
    if member_type == "present":
        new_member = present_member(
            member=member,
            profile_image=db_filename,
            degree=degree,
            department=department,
            email=email,
            interest_part=interest_part,
        )
    elif member_type == "past":
        new_member = past_member(
            member=member,
            profile_image=db_filename,
            degree=degree,
            department=department,
            email=email,
            affiliation=affiliation,
        )

    db.session.add(new_member)
    db.session.commit()
    return redirect(url_for("soda.add_page"))



# 홈 콘텐츠 추가

@soda.route("/add_home_content", methods=["POST"])
def add_home_content():

    date =  request.form.get("date")
    title =  request.form.get("title")
    content =  request.form.get("content")

    new_home_content = home_content(
                            date= date,
                            title = title,
                            content = content)
    db.session.add(new_home_content)
    db.session.commit()
    return redirect(url_for("soda.add_page"))



# 활동 사진 추가

@soda.route("/add_activity", methods=["POST"])
def add_activity():
    title  = request.form.get("title")
    date = request.form.get("date")
    people = request.form.get("people")
    venue = request.form.get("venue")
    activity_image_file = request.files.get('activity_image')
    # 2. 파일 처리: 파일이 존재하면 저장하고, 없으면 기본값 사용
    db_filename = 'default.jpg' # DB에 저장될 파일명 기본값


    if activity_image_file and activity_image_file.filename != '':
        original_filename = secure_filename(activity_image_file.filename)

    # --- 💡 여기가 수정된 부분입니다 ---
    # 파일 이름에 '.'이 있는지 확인하여 확장자를 안전하게 추출합니다.
        if '.' in original_filename:
            extension = original_filename.rsplit('.', 1)[1].lower()
        else:
        # 확장자가 없는 경우, 업로드를 거부하거나 기본 확장자를 지정할 수 있습니다.
        # 여기서는 이미지 파일이므로 임의로 'jpg'를 부여합니다.
            extension = 'jpg'
    # --- 💡 여기까지 ---

        unique_filename = str(uuid.uuid4()) + '.' + extension
        filePath = unique_filename # Supabase에 저장될 경로

        # --- 👇 여기가 수정된 부분입니다 ---
        try:
            # Supabase Storage에 업로드
            supabase.storage.from_('activity-images').upload(
                path=filePath,
                file=activity_image_file.read(),
                file_options={"content-type": activity_image_file.content_type}
            )
            # 성공 시, db에 저장할 파일명을 unique_filename으로 설정
            db_filename = unique_filename
        except Exception as e:
            print(f"Supabase 업로드 실패: {e}")
            db_filename = 'default.jpg'

        new_activity = activity_photo(
            title= title,
            activity_image=db_filename,
            date =date ,
            people=people,
            venue=venue,
        )

    db.session.add(new_activity)
    db.session.commit()
    return redirect(url_for("soda.add_page"))


@soda.route("delete_publication", methods=["POST"])
def delete_publication():
    title_to_delete = request.form['title_to_delete']
    title_obj_1 = domestic_publication.query.filter_by(title=title_to_delete).first()
    title_obj_2 = aboard_publication.query.filter_by(title=title_to_delete).first()
    if title_obj_1:
        try:
            db.session.delete(title_obj_1)
        except Exception as e:
            db.session.rollback()
    if title_obj_2:
        try:
            db.session.delete(title_obj_2)
        except Exception as e:
            db.session.rollback()
    db.session.commit()
    return redirect(url_for("soda.add_page"))


@soda.route("delete_conference", methods=["POST"])
def delete_conference():
    title_to_delete = request.form['title_to_delete']
    title_obj_1 = domestic_conference.query.filter_by(title=title_to_delete).first()
    title_obj_2 = aboard_conference.query.filter_by(title=title_to_delete).first()
    if title_obj_1:
        try:
            db.session.delete(title_obj_1)
        except Exception as e:
            db.session.rollback()
    if title_obj_2:
        try:
            db.session.delete(title_obj_2)
        except Exception as e:
            db.session.rollback()
    db.session.commit()
    return redirect(url_for("soda.add_page"))



@soda.route("delete_spec", methods=["POST"])
def delete_spec():
    title_to_delete = request.form['title_to_delete']
    member_to_delete = request.form['member_to_delete']
    obj = member_spec.query.filter_by(title=title_to_delete, member = member_to_delete).first()
    if obj:
        try:
            db.session.delete(obj)
        except Exception as e:
            db.session.rollback()
    db.session.commit()
    return redirect(url_for("soda.add_page"))




@soda.route("delete_member", methods=["POST"])
def delete_member():
    member_name_to_delete = request.form['member_to_delete']
    member_obj_1 = present_member.query.filter_by(member=member_name_to_delete).first()
    member_obj_2 = past_member.query.filter_by(member=member_name_to_delete).first()
    if member_obj_1:
        try:
            db.session.delete(member_obj_1)
        except Exception as e:
            db.session.rollback()
    if member_obj_2:
        try:
            db.session.delete(member_obj_2)
        except Exception as e:
            db.session.rollback()
    db.session.commit()
    return redirect(url_for("soda.add_page"))

@soda.route("delete_home_content", methods=["POST"])
def delete_home_content():
    title_to_delete = request.form['title_to_delete']
    obj = home_content.query.filter_by(title=title_to_delete).first()
    if obj:
        try:
            db.session.delete(obj)
        except Exception as e:
            db.session.rollback()
    db.session.commit()
    return redirect(url_for("soda.add_page"))

@soda.route("delete_activity", methods=["POST"])
def delete_activity():
    title_to_delete = request.form['title_to_delete']
    obj = activity_photo.query.filter_by(title=title_to_delete).first()
    if obj:
        try:
            db.session.delete(obj)
        except Exception as e:
            db.session.rollback()
    db.session.commit()
    return redirect(url_for("soda.add_page"))