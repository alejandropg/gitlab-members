# GitLab - Show members in a hierarchy of groups and subgroups

This is an example of how can we use the REST API of GitLab to show all the members in a hierarchy of groups, sub-groups, and projects.

Right now GitLab doesn't allow you to search a member in this kind of hierarchies, so I hope this simple code helps you to find and administer your users.

## How to use

```bash
./build.sh ; # Will create a Python virtual env and install this module dependencies
. venv/bin/activate ; # Activate the Python virtual env
python3 -m gitlab <personal-access-token> <group-name>
```

As you can see you have to pass your `<personal-access-token>` to access to the GitLab API. You can create a specific one in <https://gitlab.com/profile/personal_access_tokens>.

The second argument is the complete path name of the root group that you want to inspect.

For example in a hierarchy like:

```
organization
  John
  Laura
  sub-group
    Sara
    Marco
    project-1
      Pietro
      Berta
```

You will get an output like:

```bash
$ python -m gitlab smkcoa34rH_pl23QFKxL organization
root group - organization
    member - 837493 - john
    member - 208483 - laura
    subgroup - 8479355 - organization/sub-group
        member - 348473 - sara
        member - 483909 - marco
        project - 7893921 - project-1 - private
            member - 1230878 - pietro
            member - 499037 - berta
```

## Spanish tutorial

- <https://www.adictosaltrabajo.com/tutoriales/administrar-usuarios-gitlab-jerarquia/>
