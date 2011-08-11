#!/usr/bin/python


from Cheetah.Template import Template


fp = open("basePage.tmpl","r")
page = ""
for row in fp:
    page += row

print(page)
t = Template(page)
print(t)
